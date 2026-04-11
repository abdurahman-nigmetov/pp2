CREATE OR REPLACE FUNCTION search_phonebook(pattern_text TEXT)
RETURNS TABLE (
    id INT,
    name VARCHAR(100),
    surname VARCHAR(100),
    phone VARCHAR(20)
)
AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.name, p.surname, p.phone
    FROM phonebook p
    WHERE p.name ILIKE '%' || pattern_text || '%'
       OR p.surname ILIKE '%' || pattern_text || '%'
       OR p.phone ILIKE '%' || pattern_text || '%'
    ORDER BY p.id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_phonebook_page(limit_count INT, offset_count INT)
RETURNS TABLE (
    id INT,
    name VARCHAR(100),
    surname VARCHAR(100),
    phone VARCHAR(20)
)
AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.name, p.surname, p.phone
    FROM phonebook p
    ORDER BY p.id
    LIMIT limit_count OFFSET offset_count;
END;
$$ LANGUAGE plpgsql;