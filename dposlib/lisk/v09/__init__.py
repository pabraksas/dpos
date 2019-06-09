# -*- coding: utf-8 -*-
# © Toons

import os
import sys
import pytz
import dposlib

from datetime import datetime

from dposlib import rest
from dposlib.lisk import crypto
from dposlib.lisk.v09 import api
from dposlib.blockchain import cfg, slots, Transaction
from dposlib.util.asynch import setInterval
from dposlib.util.data import loadJson, dumpJson


TRANSACTIONS = {
	0: "send",
	1: "secondsignature",
	2: "delegate",
	3: "vote",
}
TYPING = {
	"timestamp": int,
	"type": int,
	"amount": str,
	"fee": str,
	"senderPublicKey": str,
	"recipientId": str,
	"senderId": str,
	"asset": dict,
	"signature": str,
	"signSignature": str,
	"id": str,
}


def init():
	Transaction.DFEES = False

	cfg.begintime = datetime(*cfg.begintime, tzinfo=pytz.UTC)
	resp = rest.GET.api.blocks.getNethash()
	if resp.get("success", False):
		cfg.hotmode = True
		cfg.headers["version"] = str(rest.GET.api.peers.version(returnKey="version"))
		cfg.headers["nethash"] = resp["nethash"]
		cfg.fees = rest.GET.api.blocks.getFees()["fees"]


def stop():
	pass


def broadcastTransactions(*transactions, **params):
	chunk_size = params.pop("chunk_size", 20)

	report = []
	for chunk in [transactions[i:i+chunk_size] for i in range(0, len(transactions), chunk_size)]:
		response = rest.POST.peer.transactions(transactions=chunk)
		response["ids"] = [tx["id"] for tx in chunk]
		report.append(response)

	return None if len(report) == 0 else \
		   report[0] if len(report) == 1 else \
		   report


def transfer(amount, address, vendorField=None):
	return Transaction(
		type=0,
		amount=amount*100000000,
		recipientId=address,
	)


def registerSecondSecret(secondSecret):
	raise NotImplementedError("Transaction not implemented yet")


def registerSecondPublicKey(secondPublicKey):
	raise NotImplementedError("Transaction not implemented yet")


def registerAsDelegate(username):
	raise NotImplementedError("Transaction not implemented yet")


def upVote(*usernames):
	return Transaction(
		type=3,
		asset={
			"votes": {
				"username": ["+"+rest.GET.api.delegates.get(username=username, returnKey="delegate")["publicKey"] for username in usernames]
			}
		}
	)


def downVote(*usernames):
	return Transaction(
		type=3,
		asset={
			"votes": {
				"username": ["-"+rest.GET.api.delegates.get(username=username, returnKey="delegate")["publicKey"] for username in usernames]
			}
		}
	)

