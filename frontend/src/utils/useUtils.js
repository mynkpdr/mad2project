export default function useUtils() {
    const bgQuestionTypeClass = (type) => {
        type = type ? type.toLowerCase() : type;
        if (type === 'mcq') return 'bg-danger';
        if (type === 'msq') return 'bg-info';
        if (type === 'numerical') return 'bg-primary';
        return 'bg-default';
    };

    const bgDifficultyTypeClass = (type) => {
        type = type ? type.toLowerCase() : type;
        if (type === 'easy') return 'bg-success';
        if (type === 'medium') return 'bg-warning';
        if (type === 'hard') return 'bg-danger';
        return 'bg-secondary';
    };

    const bgQuizStatusClass = (status) => {
        status = status ? status.toLowerCase() : status;
        if (status === 'live') return 'bg-success';
        if (status === 'upcoming') return 'bg-warning';
        if (status === 'completed' || status == 'expired') return 'bg-danger';
        return 'bg-secondary';
    };

    const bgQuizModeClass = (mode) => {
        mode = mode ? mode.toLowerCase() : mode;
        if (mode === 'practice') return 'bg-success';
        if (mode === 'exam') return 'bg-info';
        return 'bg-secondary';
    }

    const btnQuestionStatusClass = (status) => {
        if (!status || (status.selected_values === null && !status.answered) ) {
            return 'btn-light';
        } else if (status.markedForReview) {
            return 'btn-warning';
        } else if (status.answered) {
            return 'btn-success';
        } else {
            return 'btn-danger'
        }
    };

    const scoreStyle = (score) => {
        let width = score > 100 ? 100 : score;
        if (score >= 90) {
            return `width: ${width}%; background-color: #28a745;`;
        } else if (score >= 70) {
            return `width: ${width}%; background-color: #ffc107;`;
        } else if (score >= 50) {
            return `width: ${width}%; background-color: #17a2b8;`;
        } else if (score == null) {
            return `width: 100%; background-color: #9F9F9F;`;
        } else {
            return `width: ${width}%; background-color: #dc3545;`;
        }
    }


    const rankStyle = (rank) => {
        if (rank === 1) {
            return {
                color: "gold",
                fontSize: "1.4rem",
                backgroundColor: "rgba(255, 215, 0, 0.3)",
            };
        } else if (rank === 2) {
            return {
                color: "silver",
                fontSize: "1.2rem",
                backgroundColor: "rgba(192, 192, 192, 0.3)",
            };
        } else if (rank === 3) {
            return {
                color: "#cd7f32",
                fontSize: "1rem",
                backgroundColor: "rgba(205, 127, 50, 0.3)",
            };
        }
    };

    const getOrdinalSuffix = (number) => {
        if (number === 1) return 'st';
        if (number === 2) return 'nd';
        if (number === 3) return 'rd';
        return 'th';
    };


    return { bgQuestionTypeClass, bgDifficultyTypeClass, bgQuizModeClass, bgQuizStatusClass, btnQuestionStatusClass, rankStyle, scoreStyle, getOrdinalSuffix };
}
