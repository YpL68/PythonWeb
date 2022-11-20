QUERY_LIST = ["" for _ in range(12)]

QUERY_LIST[0] = """
    SELECT
      st.std_id AS Id,
        st.std_full_name AS Student,
        ROUND(AVG(g.grd_value),2) AS AvgGrade
    FROM grade_list AS gl
        INNER JOIN grades AS g ON gl.gls_grd_id = g.grd_id
        INNER JOIN students AS st ON gl.gls_std_id = st.std_id 
    GROUP BY
        st.std_id,
        st.std_full_name 
    ORDER BY
        AvgGrade DESC 
    LIMIT 5
"""

QUERY_LIST[1] = """
    SELECT
      st.std_id AS Id,
      st.std_full_name AS Student,
      ROUND(AVG(g.grd_value),2) AS AvgGrade
    FROM grade_list AS gl
        INNER JOIN grades AS g ON gl.gls_grd_id = g.grd_id
        INNER JOIN students AS st ON gl.gls_std_id = st.std_id 
    WHERE gls_dsc_id = 1    
    GROUP BY
        st.std_id,
        st.std_full_name 
    ORDER BY
        AvgGrade DESC, Student
    LIMIT 1
"""

QUERY_LIST[2] = """
    SELECT
        ROUND(AVG(g.grd_value ), 2) AS AvgGrade 
    FROM grade_list AS gl
        INNER JOIN grades AS g ON gl.gls_grd_id = g.grd_id 
        INNER JOIN students AS st ON gl.gls_std_id = st.std_id
    WHERE (gl.gls_dsc_id = 1 AND st.std_grp_id = 1)
"""

QUERY_LIST[3] = """
    SELECT
        ROUND(AVG(g.grd_value), 2) AS AvgGrade
    FROM grade_list AS gl
        INNER JOIN grades AS g ON gl.gls_grd_id = g.grd_id 
"""

QUERY_LIST[4] = """
    SELECT
        t.tch_name,
        d.dsc_name 
    FROM teachers AS t
        INNER JOIN disciplines AS d ON t.tch_id  = d.dsc_tch_id
    WHERE t.tch_id = 4
"""

QUERY_LIST[5] = """
    SELECT
        st.std_id AS Id,
        st.std_full_name AS Name
    FROM students AS st 
    WHERE st.std_grp_id = 3 
    ORDER BY st.std_full_name
"""

# Студенты без оценок также включены в отчет
QUERY_LIST[6] = """
    SELECT
        st.std_id,
        st.std_full_name,
        g.grd_value,
        gl.gls_date_of 
    FROM students AS st
        LEFT JOIN grade_list AS gl ON st.std_id = gl.gls_std_id AND gl.gls_dsc_id = 2
        LEFT JOIN grades g ON gl.gls_grd_id = g.grd_id 
    WHERE
        st.std_grp_id = 3
    ORDER BY st.std_id, gl.gls_date_of
"""

QUERY_LIST[7] = """
    SELECT
        st.std_id,
        st.std_full_name,
        g.grd_value,
        gl.gls_date_of 
    FROM students AS st
        INNER JOIN grade_list AS gl ON st.std_id = gl.gls_std_id AND gl.gls_dsc_id = 2
        INNER JOIN grades g ON gl.gls_grd_id = g.grd_id 
    WHERE
        (
            st.std_grp_id = 3
            and
            gl.gls_date_of = (
                SELECT 
                    MAX(gl1.gls_date_of)
                FROM grade_list AS gl1
                INNER JOIN students st1 ON gl1.gls_std_id = st1.std_id AND st1.std_grp_id = 3
                WHERE gl1.gls_dsc_id = 2)	
        )
    ORDER BY st.std_full_name
"""

# Студент попадает в отчет даже если у него еще нет оценок по предмету
QUERY_LIST[8] = """
    SELECT DISTINCT
        dc.dsc_id,
        dc.dsc_name 
    FROM grade_list AS gl
        INNER JOIN disciplines AS dc ON gl.gls_dsc_id = dc.dsc_id 
        INNER JOIN students AS st ON gl.gls_std_id = st.std_id
    WHERE 
        st.std_grp_id = (SELECT st1.std_grp_id FROM students AS st1 WHERE st1.std_id = 17)
    ORDER BY
        dc.dsc_name	
"""

QUERY_LIST[9] = """
    SELECT DISTINCT
        dc.dsc_id,
        dc.dsc_name 
    FROM grade_list AS gl
        INNER JOIN disciplines AS dc ON gl.gls_dsc_id = dc.dsc_id
        INNER JOIN students AS st ON gl.gls_std_id = st.std_id
    WHERE 
        dc.dsc_tch_id = 4
        AND
        st.std_grp_id = (SELECT st1.std_grp_id FROM students AS st1 WHERE st1.std_id = 17)
    ORDER BY
        dc.dsc_name	
"""

QUERY_LIST[10] = """
    SELECT
        ROUND(AVG(gr.grd_value), 2) AS AvgGrade
    FROM grade_list AS gl
        INNER JOIN disciplines AS dc ON gl.gls_dsc_id = dc.dsc_id
        INNER JOIN grades AS gr ON gl.gls_grd_id = gr.grd_id
    WHERE
        gl.gls_std_id = 17 
        AND 
        dc.dsc_tch_id = 4
"""

QUERY_LIST[11] = """
    SELECT
        ROUND(AVG(gr.grd_value), 2) AS AvgGrade
    FROM grade_list AS gl
        INNER JOIN disciplines AS dc ON gl.gls_dsc_id = dc.dsc_id
        INNER JOIN grades AS gr ON gl.gls_grd_id = gr.grd_id
    WHERE
        dc.dsc_tch_id = 4
"""
