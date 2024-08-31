-- postgres
SELECT 
    cc."SG_UE", 
    cc."SG_UF",
    cc."NM_UE",
    COUNT(DISTINCT cc."SQ_CANDIDATO") AS quantidade_candidatos, 
    cv."QT_VAGA",
    COUNT(DISTINCT cc."SQ_CANDIDATO")::decimal / cv."QT_VAGA" AS CandidatosPorVaga
FROM 
    public.consulta_cand_2024_brasil cc
JOIN 
    public.consulta_vagas_2024_brasil cv 
    ON cc."SG_UE" = cv."SG_UE" 
WHERE 
    cc."DS_CARGO" = \'VEREADOR\'
    AND cc."DS_ELEICAO" = \'Eleições Municipais 2024\'
    AND cv."CD_CARGO" = \'13\'
GROUP BY 
    cc."SG_UE", 
    cc."SG_UF",
    cc."NM_UE",
    cv."QT_VAGA"
ORDER BY 
    CandidatosPorVaga;