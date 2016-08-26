import winrate


def main():
    player_wins = winrate.download_current_player_wins()
    leaderboard = winrate.compute_win_rate_leaderboard(player_wins)

    for player in leaderboard:
        print(player[0], "{:.2f}%".format(player[1] * 100))

if __name__ == "__main__":
    main()