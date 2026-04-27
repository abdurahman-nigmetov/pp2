CREATE OR REPLACE FUNCTION search_phonebook(pattern_text TEXT)
RETURNS TABLE (
    id INT,
    name VARCHAR(100),
    surname VARCHAR(100),
    email VARCHAR(100),
    birthday DATE,
    group_name VARCHAR(50),
    phones TEXT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        p.id,
        p.name,
        p.surname,
        p.email,
        p.birthday,
        g.name AS group_name,
        COALESCE(string_agg(ph.phone || ' (' || ph.type || ')', ', ' ORDER BY ph.id), '')
    FROM phonebook p
    LEFT JOIN groups g ON p.group_id = g.id
    LEFT JOIN phones ph ON p.id = ph.contact_id
    WHERE p.name ILIKE '%' || pattern_text || '%'
       OR p.surname ILIKE '%' || pattern_text || '%'
       OR p.email ILIKE '%' || pattern_text || '%'
    GROUP BY p.id, p.name, p.surname, p.email, p.birthday, g.name
    ORDER BY p.id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_phonebook_page(limit_count INT, offset_count INT)
RETURNS TABLE (
    id INT,
    name VARCHAR(100),
    surname VARCHAR(100),
    email VARCHAR(100),
    birthday DATE,
    group_name VARCHAR(50),
    created_at TIMESTAMP,
    phones TEXT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        p.id,
        p.name,
        p.surname,
        p.email,
        p.birthday,
        g.name AS group_name,
        p.created_at,
        COALESCE(string_agg(ph.phone || ' (' || ph.type || ')', ', ' ORDER BY ph.id), '')
    FROM phonebook p
    LEFT JOIN groups g ON p.group_id = g.id
    LEFT JOIN phones ph ON p.id = ph.contact_id
    GROUP BY p.id, p.name, p.surname, p.email, p.birthday, g.name, p.created_at
    ORDER BY p.id
    LIMIT limit_count OFFSET offset_count;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    id INT,
    name VARCHAR(100),
    surname VARCHAR(100),
    email VARCHAR(100),
    birthday DATE,
    group_name VARCHAR(50),
    phones TEXT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        p.id,
        p.name,
        p.surname,
        p.email,
        p.birthday,
        g.name AS group_name,
        COALESCE(string_agg(ph.phone || ' (' || ph.type || ')', ', ' ORDER BY ph.id), '')
    FROM phonebook p
    LEFT JOIN groups g ON p.group_id = g.id
    LEFT JOIN phones ph ON p.id = ph.contact_id
    WHERE p.name ILIKE '%' || p_query || '%'
       OR p.surname ILIKE '%' || p_query || '%'
       OR p.email ILIKE '%' || p_query || '%'
       OR EXISTS (
            SELECT 1
            FROM phones ph2
            WHERE ph2.contact_id = p.id
              AND ph2.phone ILIKE '%' || p_query || '%'
       )
    GROUP BY p.id, p.name, p.surname, p.email, p.birthday, g.name
    ORDER BY p.id;
END;
$$ LANGUAGE plpgsql;