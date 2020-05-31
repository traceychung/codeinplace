import pandas as pd
import matplotlib.pyplot as plt
import dateutil.parser

## READ CSV FILE
# url = 'https://github.com/nytimes/covid-19-data/blob/master/us-counties.csv'
cv = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')

## ADD COUNTY_STATE COLUMN
cv['county_state'] = cv['county'] + ', ' + cv['state']

## SELECT DATA FROM LASTEST DATE
recent_date = cv['date'].max()
recent_date = str(dateutil.parser.parse(recent_date).date())
is_latest = cv['date'] == recent_date
cv_latest = cv[is_latest]

def main():
    welcome()
    top_state()
    state_data()
    top_county()
    county_data()
    goodbye()

### WELCOME MESSAGE
def welcome():
    print ("========================")
    user_input = input("Welcome! This app shows you charts for COVID-19 deaths in the US. Press any key to view top 5 deaths by state. ")
    while user_input == '':
        break
    print("========================")


### GRAPH THAT SHOWS TOP 5 DEATHS BY STATE
def top_state():
    #GROUPS HIGHEST DEATHS BY STATE
    cv_state = cv_latest.groupby(['state']).deaths.sum()
    cv_state = cv_state.reset_index()
    cv_deaths = cv_state.sort_values(by='deaths', ascending=False)
    plt.show()

    #SHOWS TOP 5 STATES
    cv_deaths = cv_deaths.head(5)
    print(cv_deaths)
    print("========================")

    #PUTS TOP 5 STATE NAMES INTO A LIST
    top_states_list = cv_deaths['state'].tolist()

    #GRAPHS TOP 5 STATES IN CHART
    states = top_states_list
    show = cv[cv['state'].isin(states)]
    show = show.loc[:, ['state', 'date', 'deaths']]
    show = show.groupby(['state', 'date']).sum()

    pvt = show.pivot_table(columns='state',index=['date'],values='deaths')
    pvt.plot(subplots=False, use_index=True)
    plt.xticks(rotation=75)
    plt.title('Top 5 States Overtime')
    plt.show()


### SHOWS STATE DATA BY USER INPUT
def state_data():
    while True:
        #ASK USER FOR STATE
        state = str(input("Which state would you like to view COVID-19 data for? Press enter to continue. "))

        #IF USER ENTERS VALID STATE, SHOW CORRESPONDING GRAPH
        if state in cv.state.values:
            cv_state = cv.loc[cv.state == state]
            cv_state =cv_state.groupby(['state','date']).deaths.sum()
            cv_state =cv_state.reset_index()
            print(cv_state)
            print("========================")
            y = cv_state['deaths']
            x = cv_state['date']
            plt.xlabel('Date'); plt.ylabel('# of Deaths')
            plt.xticks(rotation=75)
            plt.plot(x,y)
            plt.tight_layout()
            title = state + " Time Series"
            plt.title(title)
            plt.show()

        # IF USER PRESSES ENTER, MOVE ON
        elif state == '':
            break
        # IF INCORRECT SPELLING, TRY AGAIN
        else:
            print("> Sorry we couldn't find data for " + state + ". Please check your spelling and try again. ")
            print("========================")


### GRAPH THAT SHOWS TOP 5 DEATHS BY COUNTY
def top_county():
    print("========================")
    user_input = input("Now let's dig a little deeper. Press any key to view top 5 deaths by county. ")
    while user_input == '':
        break

    #GROUPS HIGHEST DEATHS BY COUNTY
    cv_county = cv_latest.groupby(['county_state']).deaths.sum()
    cv_county = cv_county.reset_index()
    cv_deaths = cv_county.sort_values(by='deaths', ascending=False)
    plt.show()

    #SHOWS TOP 5 COUNTIES
    cv_deaths = cv_deaths.head(5)
    print(cv_deaths)
    print("========================")

    #PUTS TOP 5 COUNTY NAMES INTO A LIST
    top_counties_list = cv_deaths['county_state'].tolist()

    #GRAPH OF TOP 5 DEATHS / COUNTY
    county_states = top_counties_list
    show = cv[cv['county_state'].isin(county_states)]
    show = show.loc[:, ['county_state', 'date', 'deaths']]
    show = show.groupby(['county_state', 'date']).sum()

    pvt = show.pivot_table(columns='county_state', index=['date'], values='deaths')
    pvt.plot(subplots=False, use_index=True)
    plt.xticks(rotation=75)
    plt.title('Top 5 Counties Overtime')
    plt.show()

### SHOWS COUNTY DATA BY USER INPUT
def county_data():
    while True:
        #ASK USER FOR COUNTY
        user_county = str(input("Which county would you like to view COVID-19 data for? Please enter 'full county, full state'. Press enter once done. "))
        #IF VALID COUNTY, SHOWS CORRESPONDING GRAPH
        if user_county in cv.county_state.values:
            cv_county = cv.loc[cv.county_state == user_county]
            cv_county = cv_county.loc[:, ['county_state', 'date', 'deaths']]
            print(cv_county)
            print("========================")
            y = cv_county['deaths'];
            x = cv_county['date']
            plt.xlabel('Date'); plt.ylabel('# of Deaths')
            plt.xticks(rotation=75)
            plt.plot(x,y)
            title = user_county + " Time Series"
            plt.title(title)
            plt.tight_layout()
            plt.show()

        #IF USER PRESSES ENTER, MOVE ON
        elif user_county == '':
            break

        # IF INCORRECT SPELLING, TRY AGAIN
        else:
            print("> Sorry we couldn't find data for " + user_county + ". Please check your spelling and try again. ")
            print("========================")

#GOODBYE MESSAGE
def goodbye():
    print("========================")
    print("Thanks for using this app! Please continue to social distance, wash your hands, and be safe. We're all in this together! ")
    print("========================")

if __name__ == '__main__':
    main()
