from algorithms.sac import SAC
from algorithms.sac_aug import SAC_AUG
from algorithms.soda import SODA
from algorithms.soda_aug import SODA_AUG
from algorithms.drq import DrQ
from algorithms.drq_aug import DrQ_AUG
from algorithms.svea import SVEA
from algorithms.svea_aug import SVEA_AUG

algorithm = {
	'sac': SAC,
	'sac_aug':SAC_AUG,
	'soda': SODA,
	'soda_aug':SODA_AUG,
	'drq': DrQ,
	'drq_aug': DrQ_AUG,
	'svea':SVEA,
	'svea_aug':SVEA_AUG
}


def make_agent(obs_shape, action_shape, args):
	return algorithm[args.algorithm](obs_shape, action_shape, args)
