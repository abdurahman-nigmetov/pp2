CREATE OR REPLACE PROCEDURE upsert_contact(
    p_name VARCHAR(100),
    p_surname VARCHAR(100),
    p_email VARCHAR(100),
    p_birthday DATE,
    p_group_id INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM phonebook
        WHERE name = p_name AND surname = p_surname
    ) THEN
        UPDATE phonebook
        SET email = p_email,
            birthday = p_birthday,
            group_id = p_group_id
        WHERE name = p_name AND surname = p_surname;
    ELSE
        INSERT INTO phonebook(name, surname, email, birthday, group_id)
        VALUES (p_name, p_surname, p_email, p_birthday, p_group_id);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE insert_many_contacts(
    IN p_names TEXT[],
    IN p_surnames TEXT[],
    IN p_emails TEXT[],
    IN p_birthdays DATE[],
    IN p_group_ids INTEGER[],
    INOUT incorrect_data TEXT[] DEFAULT '{}'
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
BEGIN
    IF array_length(p_names, 1) <> array_length(p_surnames, 1)
       OR array_length(p_names, 1) <> array_length(p_emails, 1)
       OR array_length(p_names, 1) <> array_length(p_birthdays, 1)
       OR array_length(p_names, 1) <> array_length(p_group_ids, 1) THEN
        RAISE EXCEPTION 'Arrays must have same length';
    END IF;

    FOR i IN 1..array_length(p_names, 1) LOOP
        IF p_names[i] = '' OR p_surnames[i] = '' THEN
            incorrect_data := array_append(
                incorrect_data,
                coalesce(p_names[i], '') || ':' || coalesce(p_surnames[i], '')
            );

        ELSIF p_emails[i] IS NOT NULL
           AND p_emails[i] <> ''
           AND p_emails[i] !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' THEN
            incorrect_data := array_append(
                incorrect_data,
                p_names[i] || ':' || p_surnames[i] || ':' || p_emails[i]
            );

        ELSE
            CALL upsert_contact(
                p_names[i],
                p_surnames[i],
                NULLIF(p_emails[i], ''),
                p_birthdays[i],
                p_group_ids[i]
            );
        END IF;
    END LOOP;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_contact(p_value TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE name = p_value
       OR surname = p_value
       OR email = p_value;
END;
$$;


CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    SELECT id
    INTO v_contact_id
    FROM phonebook
    WHERE name = p_contact_name
    ORDER BY id
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact with name "%" not found', p_contact_name;
    END IF;

    IF p_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'Phone type must be home, work, or mobile';
    END IF;

    IF p_phone !~ '^[0-9+\-() ]{5,20}$' THEN
        RAISE EXCEPTION 'Invalid phone format';
    END IF;

    INSERT INTO phones(contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);
END;
$$;


CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_group_id INTEGER;
BEGIN
    INSERT INTO groups(name)
    VALUES (trim(p_group_name))
    ON CONFLICT (name) DO NOTHING;

    SELECT id
    INTO v_group_id
    FROM groups
    WHERE name = trim(p_group_name);

    UPDATE phonebook
    SET group_id = v_group_id
    WHERE name = p_contact_name;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Contact with name "%" not found', p_contact_name;
    END IF;
END;
$$;