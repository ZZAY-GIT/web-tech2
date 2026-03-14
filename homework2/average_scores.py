def compute_average_scores(scores):
    if not scores:
        return ()
    
    N = len(scores[0])
    X = len(scores)
    
    student_sums = [0] * N
    for subject_scores in scores:
        for i in range(N):
            student_sums[i] += subject_scores[i]

    averages = tuple(round(total / X, 1) for total in student_sums)
    
    return averages


if __name__ == "__main__":

    first_line = input().strip()
    N, X = map(int, first_line.split())

    scores = []
    for _ in range(X):
        line = input().strip()
        subject_scores = tuple(map(float, line.split()))
        scores.append(subject_scores)
    

    averages = compute_average_scores(scores)

    for avg in averages:
        print(f"{avg:.1f}")