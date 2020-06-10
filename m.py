import pandas as pd
import sys

def isstrint(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

Stat_df = pd.read_csv('stat.csv')
out_df = pd.DataFrame(columns=['Date'])
#sett_df = pd.DataFrame()
sett_df = pd.read_csv('sett_df.csv')

TransRowID = 0

def addCols(col):
	global out_df
	out_df[col[0]] = '0'

def start(trans):
	global out_df, sett_df, TransRowID, TransSuccess
	TransSuccess = 0
	
	if not sum(out_df["Date"].astype("str").str.contains(trans[0])) > 0 :
		out_df = out_df.append({'Date' : [trans[0]]}, ignore_index=True)
	
	sett_df['length'] = sett_df['find'].str.len()
	sett_df.sort_values('length', ascending=False, inplace=True)
	#CHeck transaction for matches 
	while TransSuccess == 0:
		sett_df.apply(checkRows, axis=1)

		#if the transaction hasnt been categorised yet:
		if TransSuccess == 0 :
			#repeat asking for a valid MatchPhrase untill broken by a worthy MatchPhrase
			#while True:

			#print tranaction address
			print(Stat_df.iloc[TransRowID,2])
			print(" of ")
			#print tranaction amount 
			print(Stat_df.iloc[TransRowID,1])
			print("MatchPhrase = ")
			#MatchPhrase = the part of the address that should be looked for the transaction to categorize it
			MatchPhrase = input()

			if MatchPhrase == "exit" :
				#save output file and settings file
				out_df.to_csv('text.csv', index=False)
				sett_df.to_csv('sett_df.csv', index=False)
				#exit program
				sys.exit()

			#make sure that MatchPhrase is in the trasaction address AND isnt empty
			#if MatchPhrase in Stat_df.iloc[TransRowID,2] and not MatchPhrase == "":
				#break asking for the correct MatchPhrase
				#break

			#print existing outputed columns
			print(sett_df.col.drop_duplicates())
			print("Name new col, or refrence existing by id:")
			NewCol = input()

			#check if user wants to exit program 
			if NewCol == "exit" or MatchPhrase == "exit" :
				#save output file and settings file
				out_df.to_csv('text.csv', index=False)
				sett_df.to_csv('sett_df.csv', index=False)
				#exit program
				sys.exit()

			# NOT SURE 
			out_df[NewCol] = '0'

			#if NewCol is a number
			if isstrint(NewCol):
				#add MatchPhrase to settings file dataframe (sett_df) and use the same col name as the NewCol'nth row
				sett_df = sett_df.append({'find':MatchPhrase, 'col':sett_df.iloc[int(NewCol),0]}, ignore_index=True)
			else:
				# else : add MatchPhrase to settings file dataframe (sett_df) using the col name NewCol
				sett_df = sett_df.append({'find':MatchPhrase, 'col':NewCol}, ignore_index=True)

			# i think, if last row has content or if last row exists ... idk
			if out_df.isnull().iloc[-1,1] :
				#write trasaction amount to output file
				out_df.loc[out_df.index[-1], NewCol] = str(Stat_df.iloc[TransRowID,1])
			else:
				#add amount to the existing cols content 
				out_df.loc[out_df.index[-1], NewCol] = str(out_df.iloc[-1, 1]) + ", " + str(Stat_df.iloc[TransRowID,1])

	TransRowID = TransRowID + 1
	
	
def checkRows(Rule):
	global TransRowID, sett_df, TransSuccess
	#if not yet succesful 
	if TransSuccess == 0:
		#if rules find col matches any part of the trasaction 
		if str(Rule[1]) in str(Stat_df.iloc[TransRowID,2]):
			print (Rule[0] + " - " + Stat_df.iloc[TransRowID,2] + " - " + Rule[1])
			TransSuccess = 1
			if out_df.isnull().iloc[-1,1] or out_df.iloc[-1,1] == "0" :
				out_df.loc[out_df.index[-1], Rule[0]] = str(Stat_df.iloc[TransRowID,1])
			else:
				out_df.loc[out_df.index[-1], Rule[0]] = str(out_df.iloc[-1, 1]) + ", " + str(Stat_df.iloc[TransRowID,1])


#Build Columns
sett_df.apply(addCols, axis=1)
#filter every transaction
Stat_df.apply(start, axis=1)

out_df.to_csv('text.csv', index=False)
sett_df.to_csv('sett_df.csv', index=False)
