from django.apps import AppConfig
from django.db import connection


class StreeterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'streeter'

    def ready(self):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                create or replace function get_shops(is_open boolean)
                    returns setof streeter_shop
                    language plpgsql as
                $$
                begin
                    declare
                        opened         streeter_shop[];
                        closed         streeter_shop[];
                        raw            streeter_shop%rowtype;
                        cur_time       timestamp;
                        new_close_time timestamp;
                    begin
                        cur_time := now()::timestamp;
                        for raw in select * from streeter_shop
                            loop
                                if raw.open_time > raw.close_time then
                                    new_close_time := raw.close_time + cur_time::date;
                                    new_close_time := new_close_time + interval '1 day';
                                    if ((raw.open_time < cur_time::time) AND (new_close_time > cur_time)) then
                                        opened := array_append(opened, raw);
                                    else
                                        closed := array_append(closed, raw);
                                    end if;
                                else
                                    if ((raw.open_time < cur_time::time) AND (raw.close_time > cur_time::time)) then
                                        opened := array_append(opened, raw);
                                    else
                                        closed := array_append(closed, raw);
                                    end if;
                                end if;
                            end loop;


                        if is_open then
                            foreach raw in array opened
                                loop
                                    return next raw;
                                end loop;
                        else
                            foreach raw in array closed
                                loop
                                    return next raw;
                                end loop;
                        end if;
                    end;
                end;
                $$;
                """)
                cursor.close()
        except Exception as e:
            print("Выполниться удачно во время запуска сервера")
            # exit(1)
