__author__ = 'bartselen'
__version__ = '1.0'
'''
Ticket Status:
 4 - Closed
 5 - Unclaimed
 Other - Claimed
 None - Error

'''
import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton
import System
from datetime import datetime

class ModRequest:
	def SendNewTicketMessageToMods(msg, sender, id):
		for pl in Server.Players:
			if pl.Admin:
				pl.Message("--New Ticket Submitted--")
				pl.Message("Sender: " + sender.Name)
				pl.Message("Ticket: " + request)
				pl.Message("ID: " + id)
				pl.Message("Use /claim <id> to claim this ticket")
				
	def On_Command(self, cmd):
		command = cmd.cmd
		player = cmd.User
		args = cmd.args
		
		if command == "time":
			player.MessageFrom("PEssentials", "The current time is" + str(datetime.now().strftime('%H:%M:%S')) + ".")
			
		elif command == "modreq":	
			if len(args) > 0:
			
				request = str.Join(" ", args)
				ticketID = 0
				latestActiveID = DataStore.Get("Active", "LatestActiveID")
				if not isinstance(latestActiveID, int) or not latestActiveID == None:
					return
					
				ticketID = int(latestActiveID) + 1
				if latestActiveID is None:
					ticketID = 1
				'''
				except error:
					player.Message("Error submitting ticket.")
					return 
				'''
				
				DataStore.Add("Active", "LatestActiveID", ticketID)
				DataStore.Save()
				DataStore.Add("ActiveTicketsID", ticketID, request)
				DataStore.Save()
				DataStore.Add("ActiveTicketsSender", ticketID, player.SteamID)
				DataStore.Save()
				DataStore.Add("ActiveTicketsClaimed", ticketID, 5)
				DataStore.Save()
				if DataStore.Get("ActivePlayerTickets", player.SteamID) == None:
					DataStore.Add("ActivePlayerTickets", player.SteamID, ticketID)
					DataStore.SaveAll()
				else:
					DataStore.Add("ActivePlayerTickets", player.SteamID, (str(DataStore.Get("ActivePlayerTickets", player.SteamID)) + ":" + str(ticketID)))
					DataStore.SaveAll()
				self.SendNewTicketMessageToMods(request, player, ticketID)
				
			elif len(args) == 0:
				player.Message("Wrong usage: use /modreq <message>")
				
		elif command == "claim":
			if player.Admin:
				if len(args) == 1:
					if isinstance(args[0], int):
						if DataStore.Get("ActiveTicketsClaimed", args[1]) != None:
							if DataStore.Get("ActiveTicketsClaimed", args[1]) == 5:
								DataStore.Add("ActiveTicketsClaimed", args[1], player.SteamID)
								DataStore.SaveAll()
								player.Message("You have claimed the ticket with an id of" + args[0])
							elif DataStore.Get("ActiveTicketsClaimed", args[1]) == 4:
								player.Message("The specified ticket has already been closed")
							else:
								player.Message("The specified ticket has already been claimed")
					# elif canoverride:
					
		elif command == "status":
			if DataStore.Get("ActivePlayerTickets", player.SteamID) != None:
				if not ":" in str(DataStore.Get("ActivePlayerTickets", player.SteamID)):
					id = int(DataStore.Get("ActivePlayerTickets", player.SteamID))
					if DataStore.Get("ActiveTicketsClaimed", id) == 5:	
						player.Message("Tickets submitted by you:")
						player.Message("    ID    |        Status         ")
						player.Message('{:^10}'.format(str(id)) + "|" + '{:^25}'.format("Pending"))
					elif DataStore.Get("ActiveTicketsClaimed", id) == 4:
						player.Message("Tickets submitted by you:")
						player.Message("    ID    |        Status         ")
						player.Message('{:^10}'.format(str(id)) + "|" + '{:^25}'.format("Closed"))
					else:
						if DataStore.Get("ActiveTicketsClaimed", id) != None:
							player.Message("Tickets submitted by you:")
							player.Message("    ID    |        Status         ")
							player.Message('{:^10}'.format(str(id)) + "|" + '{:^25}'.format("Claimed by " + str(DataStore.Get("ActiveTicketsClaimed", id))))
				else:
					ids = DataStore.Get("ActivePlayerTickets", player.SteamID).split(":")
					for id in ids:
						player.Message("Tickets submitted by you:")
						player.Message("    ID    |        Status         ")
						if DataStore.Get("ActiveTicketsClaimed", id) == 5:	
							player.Message('{:^10}'.format(str(id)) + "|" + '{:^25}'.format("Pending"))
						elif DataStore.Get("ActiveTicketsClaimed", id) == 4:
							player.Message('{:^10}'.format(str(id)) + "|" + '{:^25}'.format("Closed"))
						else:
							if DataStore.Get("ActiveTicketsClaimed", id) != None:
								player.Message('{:^10}'.format(str(id)) + "|" + '{:^25}'.format("Claimed by " + str(DataStore.Get("ActiveTicketsClaimed", id))))
			else:
				player.Message("You haven't submitted any tickets")
