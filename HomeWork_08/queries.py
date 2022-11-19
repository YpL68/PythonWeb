query_1 = """
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

query_2 = """
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

query_3 = """
    SELECT
        ROUND(AVG(g.grd_value ), 2) AS AvgGrade 
    FROM grade_list AS gl
        INNER JOIN grades AS g ON gl.gls_grd_id = g.grd_id 
        INNER JOIN students AS st ON gl.gls_std_id = st.std_id
    WHERE (gl.gls_dsc_id = 1 AND st.std_grp_id = 1)
"""

query_4 = """
    SELECT
        ROUND(AVG(g.grd_value), 2) AS AvgGrade
    FROM grade_list AS gl
        INNER JOIN grades AS g ON gl.gls_grd_id = g.grd_id 
"""

query_5 = """
    SELECT
        t.tch_name,
        d.dsc_name 
    FROM teachers AS t
        INNER JOIN disciplines AS d ON t.tch_id  = d.dsc_tch_id
    WHERE t.tch_id = 4
"""

query_6 = """
    SELECT
        st.std_id AS Id,
        st.std_full_name AS Name
    FROM students AS st 
    WHERE st.std_grp_id = 3 
    ORDER BY st.std_full_name
"""

query_7 = """
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

query_8 = """
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
                INNER JOIN students st1 ON gl1.gls_std_id = st1.std_id and st1.std_grp_id = 3
                WHERE gl1.gls_dsc_id = 2)	
        )
    ORDER BY st.std_full_name
"""

query_9 = """
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
