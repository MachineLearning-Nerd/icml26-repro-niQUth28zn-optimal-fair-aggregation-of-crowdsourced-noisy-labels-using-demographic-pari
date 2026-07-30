import numpy as np


ETA = 0.4688


def sample_population(n, p_a1, q, seed):
    rng = np.random.default_rng(seed)
    sensitive = (rng.random(n) < p_a1).astype(np.int8)
    positive_rate = np.where(sensitive == 1, q[1], q[0])
    labels = (rng.random(n) < positive_rate).astype(np.int8)
    return sensitive, labels


def annotator_labels(sensitive, labels, skills, seed, bias=None):
    rng = np.random.default_rng(seed)
    skills = np.asarray(skills, dtype=float)
    correct = rng.random((labels.size, skills.size)) < skills
    votes = np.where(correct, labels[:, None], 1 - labels[:, None]).astype(np.int8)
    if bias is not None:
        bias = np.asarray(bias, dtype=float)
        promote = (
            (sensitive[:, None] == 1)
            & (votes == 0)
            & (rng.random(votes.shape) < bias)
        )
        votes[promote] = 1
    return votes


def majority_vote(votes):
    return (votes.sum(axis=1) >= votes.shape[1] / 2).astype(np.int8)


def delta_dp(labels, sensitive):
    return float(labels[sensitive == 1].mean() - labels[sensitive == 0].mean())


def accuracy(predictions, labels):
    return float((predictions == labels).mean())


def k_mv(skills):
    skills = np.asarray(skills, dtype=float)
    log_t = np.linspace(-12.0, 0.0, 20_001)
    t = np.exp(log_t)[:, None]
    objective = np.log(skills[None, :] * t + (1 - skills)[None, :] / t).mean(axis=1)
    return float(-objective.min())


def prop36_bound(votes, sensitive):
    rates = np.stack(
        [votes[sensitive == group].mean(axis=0) for group in (0, 1)]
    )
    variances = (rates * (1 - rates)).sum(axis=1)
    epsilon_r = ETA / np.sqrt(variances.min())
    individual_gap_sum = np.abs(rates[1] - rates[0]).sum()
    return float(epsilon_r * individual_gap_sum), float(epsilon_r), float(individual_gap_sum)


def competent_majority(skills, eps, lower_bound):
    skills = np.asarray(skills, dtype=float)
    competent = np.count_nonzero(skills >= 0.5 + eps)
    adversarial = np.count_nonzero(
        (skills >= lower_bound) & (skills <= 0.5 - eps)
    )
    condition = competent / skills.size * (1 + 2 * eps)
    condition += 2 * lower_bound * adversarial / skills.size
    return float(condition), bool(condition > 1)


def faircrowd(posterior, sensitive, group_probability, epsilon):
    signs = np.where(sensitive == 1, 1.0, -1.0)
    group_probability = np.asarray(group_probability, dtype=float)
    denominator = 2 * group_probability[sensitive]
    beta_grid = np.linspace(-1, 1, 20_001)
    beta_grid = beta_grid[np.argsort(np.abs(beta_grid), kind="stable")]
    for beta in beta_grid:
        prediction = (posterior >= 0.5 + signs * beta / denominator).astype(np.int8)
        gap = abs(delta_dp(prediction, sensitive))
        if gap <= epsilon:
            return prediction, float(beta), float(gap)
    raise RuntimeError("No epsilon-fair threshold found")
