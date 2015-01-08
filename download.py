order_filter = "Humble Image Comics Bundle 2"
requested_type = "PDF"

DOWNLOAD_COMMAND = "wget --continue -O '$name' '$url'"

import humblebundle
import os.path

client = humblebundle.HumbleApi()
client.login("username@example.com", "secret")

order_list = client.order_list()

download_script = "#!/bin/sh"
hashes = {"sha1": "", "md5": ""}


for order in filter(lambda o: order_filter in o.product.human_name, order_list):
	print "  " + order.product.human_name
	for product in order.subproducts:
		print "    " + product.human_name
		dls = [dl2 for dl in product.downloads for dl2 in dl.download_struct if dl2.name == requested_type]
		print "      found " + str(len(pdfs)) + " matching downloads"
		if len(dls) == 0:
			print "      WARN: No downloads found for this product :-("
		for dl in dls:
			url = dl.url.web
			filename = product.machine_name + "-" + os.path.basename(url).split("?")[0]
			download_script += "\n" + \
				DOWNLOAD_COMMAND.replace("$name", filename).replace("$url", url)
			hashes_found = 0
			for hash_type in hashes.keys():
				h = getattr(dl, hash_type, None)
				if h:
					hashes[hash_type] += h + "  " + filename + "\n"
					hashes_found += 1
			if hashes_found == 0:
				print "      WARN: No hahes found for %s" % filename

with open("download.sh", "w") as f:
	f.write(download_script)

for hash_type in hashes.keys():
	with open(hash_type + "sums", "w") as f:
		f.write(hashes[hash_type])

