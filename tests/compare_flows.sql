WITH original as (SELECT django_oemof_simulation.id,
                         django_oemof_simulation.scenario,
                         from_node,
                         to_node,
                         (SELECT SUM(val)
                          FROM unnest(doos.value[1:array_length(doos.value, 1) - 1]) AS val) AS total_value,
                         array_length(doos.value, 1)
                  FROM django_oemof_simulation
                           JOIN public.django_oemof_oemofdataset doo
                                ON django_oemof_simulation.dataset_id = doo.id
                           JOIN public.django_oemof_oemofdata dood
                                ON doo.result_id = dood.id
                           JOIN public.django_oemof_oemofdata_sequences doods
                                ON dood.id = doods.oemofdata_id
                           JOIN public.django_oemof_oemofsequence doos
                                ON doods.oemofsequence_id = doos.id
                  WHERE django_oemof_simulation.id = 18),
    tsam as (
       SELECT django_oemof_simulation.id,
                         django_oemof_simulation.scenario,
                         from_node,
                         to_node,
                         (SELECT SUM(val)
                          FROM unnest(doos.value[1:array_length(doos.value, 1) - 1]) AS val) AS total_value,
                         array_length(doos.value, 1)
                  FROM django_oemof_simulation
                           JOIN public.django_oemof_oemofdataset doo
                                ON django_oemof_simulation.dataset_id = doo.id
                           JOIN public.django_oemof_oemofdata dood
                                ON doo.result_id = dood.id
                           JOIN public.django_oemof_oemofdata_sequences doods
                                ON dood.id = doods.oemofdata_id
                           JOIN public.django_oemof_oemofsequence doos
                                ON doods.oemofsequence_id = doos.id
                  WHERE django_oemof_simulation.id = 37
    )
SELECT
    tsam.from_node,
    tsam.to_node,
    original.total_value,
    tsam.total_value,
    CASE WHEN original.total_value > 0 THEN tsam.total_value - original.total_value ELSE 0 END AS difference,
    CASE WHEN original.total_value > 0 THEN (tsam.total_value - original.total_value) / original.total_value * 100 ELSE 0 END AS percentage
FROM original
FULL OUTER JOIN tsam ON original.from_node = tsam.from_node AND original.to_node = tsam.to_node
