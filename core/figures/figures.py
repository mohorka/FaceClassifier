import matplotlib.pyplot as plt
from core.config.config import RESULTS_PATH

def corr_num_ref_plot(best_scores):
    params = [p for _, p in best_scores]
    scores = [s for s, _ in best_scores]

    plt.plot(params, scores)
    plt.xlabel('param')
    plt.ylabel('score')
    plt.figtext(0, 0.95, f'Best score: {max(scores)}', fontsize=10)
    plt.title("Relation between accuracy and params' value")
    plt.figtext(
        0,
        0.92,
        f'Parameter: '
        f'{[p for s, p in best_scores if s==max(scores)][0]}'
    )
    plt.savefig(''.join([RESULTS_PATH,'result.png']))
    plt.figure().clear()

def multi_features_amount_plot(best_scores):
    train_size = [t for t,_ in best_scores]
    scores = [s for _,s in best_scores]

    plt.plot(train_size, scores)
    plt.xlabel('train size')
    plt.ylabel('score')
    plt.title("Amount influence on parallel system perfomance")
    plt.savefig(''.join([RESULTS_PATH,'parallel_res.png']))
    plt.figure().clear()

def corr_amount_accuracy_plot(scores):
    amount = [a for a, _ in scores]
    accuracy = [ac for _, ac in scores]

    plt.plot(amount, accuracy)
    plt.xlabel('Images amount')
    plt.ylabel('Accuracy')
    plt.title('Perfomance of parallel system')
    plt.savefig(''.join([RESULTS_PATH, 'parallel_res.png']))
    plt.figure().clear()

