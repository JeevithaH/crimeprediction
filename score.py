def pred_score(year, predicted_crimes_2024):
    rate = None

    if year == "2024":
        if predicted_crimes_2024 < 840:
            rate = "low ✅"
        elif 840 < predicted_crimes_2024 < 3875:
            rate = "medium 🟡"
        else:
            rate = "high ☠️"
    elif year == "2025":
        if predicted_crimes_2024 < 822:
            predicted_crimes_2024 += 18
            rate = "low ✅"
        elif 840 < predicted_crimes_2024 < 3799:
            predicted_crimes_2024 += 76
            rate = "medium 🟡"
        else:
            predicted_crimes_2024 += 103
            rate = "high ☠️"
    elif year == "2026":
        if predicted_crimes_2024 < 815:
            predicted_crimes_2024 += 25
            rate = "low ✅"
        elif 840 < predicted_crimes_2024 < 3796:
            predicted_crimes_2024 += 79
            rate = "medium 🟡"
        else:
            predicted_crimes_2024 += 109
            rate = "high ☠️"

    return rate, predicted_crimes_2024
