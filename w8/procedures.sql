CREATE OR REPLACE PROCEDURE upsert_contact(
    p_name VARCHAR(100),
    p_surname VARCHAR(100),
    p_phone VARCHAR(20)
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM phonebook
        WHERE name = p_name AND surname = p_surname
    ) THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE name = p_name AND surname = p_surname;
    ELSE
        INSERT INTO phonebook(name, surname, phone)
        VALUES (p_name, p_surname, p_phone);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE insert_many_contacts(
    IN p_names TEXT[],
    IN p_surnames TEXT[],
    IN p_phones TEXT[],
    INOUT incorrect_data TEXT[] DEFAULT '{}'
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
BEGIN
    IF array_length(p_names, 1) <> array_length(p_phones, 1)
       OR array_length(p_names, 1) <> array_length(p_surnames, 1) THEN
        RAISE EXCEPTION 'Arrays must have same length';
    END IF;

    FOR i IN 1..array_length(p_names, 1) LOOP
        IF p_names[i] = '' OR p_surnames[i] = '' OR p_phones[i] = '' THEN
            incorrect_data := array_append(
                incorrect_data,
                p_names[i] || ':' || p_surnames[i] || ':' || p_phones[i]
            );

        ELSIF p_phones[i] !~ '^[0-9+\-() ]{5,20}$' THEN
            incorrect_data := array_append(
                incorrect_data,
                p_names[i] || ':' || p_surnames[i] || ':' || p_phones[i]
            );

        ELSE
            CALL upsert_contact(p_names[i], p_surnames[i], p_phones[i]);
        END IF;
    END LOOP;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_contact(p_value TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE name = p_value OR surname = p_value OR phone = p_value;
END;
$$;