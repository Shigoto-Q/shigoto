-- EXECUTE ONLY ONCE!

CREATE OR REPLACE FUNCTION notify_event()
    RETURNS TRIGGER AS $$
DECLARE
    subscribed_user_id integer;
    data json;
    notification json;
    result json;
BEGIN
    SELECT json_agg(tmp)
    INTO data
    FROM (
             SELECT * FROM tasks_taskresult
             WHERE tasks_taskresult.user_id = subscribed_user_id
         ) tmp;

    result := json_build_object('data', data, 'row', row_to_json(NEW));

    PERFORM pg_notify('events', result::text);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
