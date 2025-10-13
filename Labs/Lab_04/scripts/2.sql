DROP AGGREGATE IF EXISTS concat_comments_agg(TEXT);
DROP FUNCTION IF EXISTS agg_concat_comments_state(TEXT, TEXT);
DROP FUNCTION IF EXISTS agg_concat_comments_final(TEXT);

CREATE OR REPLACE FUNCTION agg_concat_comments_state(state TEXT, val TEXT)
RETURNS TEXT
LANGUAGE plpython3u
AS $$

if state is None:
    if val is None:
        return ''
    else:
        return val

if val is None or val.strip() == '':
    return state
return state + '\x01' + val
$$;

CREATE OR REPLACE FUNCTION agg_concat_comments_final(state TEXT)
RETURNS TEXT
LANGUAGE plpython3u
AS $$

if state is None or state == '':
    return None
parts = [p.strip() for p in state.split('\x01') if p and p.strip() != '']

if not parts:
    return None

return '; '.join(parts)
$$;

CREATE AGGREGATE concat_comments_agg(TEXT) (
    sfunc = agg_concat_comments_state,
    stype = TEXT,
    finalfunc = agg_concat_comments_final,
    initcond = ''
);

SELECT concat_comments_agg(comment) AS all_comments
FROM Records
WHERE specialist_id = 1;
