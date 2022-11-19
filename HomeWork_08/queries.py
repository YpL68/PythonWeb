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
