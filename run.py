import pages.rankings as rankings

def main():
    get_rankings()
    
def get_rankings():
    rankings.populate_rankings()

if __name__ == "__main__":
    main()