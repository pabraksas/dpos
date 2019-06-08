# -*- coding: utf-8 -*-
# © Toons
# ~ https://docs.ark.io/archive/api/public-v1/

from dposlib.blockchain import Wallet, Data


# def transactions(self, limit=50):
# 	received, sent, count = [], [], 0
# 	while count < limit:
# 		sent.extend(dposlib.rest.GET.api.transactions(senderId=self.address, orderBy="timestamp:desc", returnKey="transactions", offset=len(sent)))
# 		received.extend(dposlib.rest.GET.api.transactions(recipientId=self.address, orderBy="timestamp:desc", returnKey="transactions", offset=len(received)))
# 		tmpcount = len(sent)+len(received)
# 		count = limit if count == tmpcount else tmpcount
# 	return [filter_dic(dic) for dic in sorted(received+sent, key=lambda e:e.get("timestamp", None), reverse=True)[:limit]]


class Delegate(Data):
	
	def __init__(self, username, **kw):
		Data.__init__(self, dposlib.rest.GET.api.delegates.get, **dict({"username":username, "returnKey":"delegate"}, **kw))

	def getWallet(self):
		return Wallet(self.address)

	def forged(self):
		result = filter_dic(dposlib.rest.GET.api.delegates.forging.getForgedByAccount(generatorPublicKey=self.publicKey))
		result.pop("success", False)
		return result

	def voters(self):
		voters = [a for a in dposlib.rest.GET.api.delegates.voters(publicKey=self.publicKey, returnKey="accounts") if a["balance"] not in [0, "0"]]
		return list(sorted([filter_dic(dic) for dic in voters], key=lambda e:e["balance"], reverse=True))
	
	def lastBlock(self):
		blocks = [blk for blk in dposlib.rest.GET.api.blocks(returnKey="blocks") if blk["generatorId"] == self.address]
		if len(blocks):
			return Block(blocks[0]["id"])


class Block(Data):

	def __init__(self, blk_id, **kw):
		Data.__init__(self, dposlib.rest.GET.api.blocks.get, **dict({"id":blk_id, "returnKey":"block"}, **kw))

	def previous(self):
		return Block(self.previousBlock)

	def transactions(self):
		return dposlib.rest.GET.api.transactions(blockId=self.id, returnKey="transactions")
