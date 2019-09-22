## Tesseract Note

### How To Use
1. Install docker-ce [link](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
2. Download ready to deploy tesseract docker: `docker push fatchur/tesseract:v1`
3. **NOTE**: This docker is working well for ubuntu 18.04 (bionic)
4. Run the downloaded docker image: `sudo docker run -d -p 8080:8080 <image name>:v1`
5. **NOTE**: Now your service is up

### Sending A Request
After deploying your docker, you can send a request to the tesseract service with the following format:
```
{"image": "base64 document image"}
```
The endpoint:
```
http://127.0.0.1:8080/get_text
```

The Response:
```
{
    "text": "Fantasi-Nyata Afrika\ndari si Raja Kartun\n\n \n\nJudul: The Lion King\nSutradara: Roger Allers, Rob Minkoff\nCerita: Brenda Chapman\nTokoh: Simba, Mufasa, Scar, Nala, Rafiki,\n\nPumbaa,\nProduksi: Walt Disney Pictures\n\nTimon\n\n \n\nSETELAH menghasilkan 31\nfilm kartun berdasarkan kisah\nKlasik terkenal dunia, melalui\nThe Lion King inilah kali perta-\nma Walt Disney Pictures mem-\nbuat film kartun berdasarkan ce-\nrita asli. Mengambil setting ke-\nhidupan belantara Afrika, sekali\nlagi Disney membuktikan kepia-\nwaiannya sebagai raja kartun\ndunia.\n\nFilm dibuka dengan upacara\npenobatan Simba, bocah singa\nputra Raja Mufasa, sebagai pu-\ntra mahkota kerajaan Pride\nLands. Penonton kemudian di-\nperkenalkan dengan Paman Scar,\nsaudara Mufasa yang tidak rela\ntahta Pride Lands diduduki Mu-\nfasa dan akan jatuh ke tangan\nSimba.\n\nDengan bantuan tiga hyena (se-\njenis serigala Afrika), Scar meny-\n\nusun rencana menjebak Simba..\n\nSebagai singa kecil yang belum\n\nberpengalaman, dengan mudah\n\nSimba termakan kelicikan sang\n\npaman dan terjebak dalam kepu-\nan ribuan penghuni hutan.\n\niu sang putra dalam baha-\n\nee se ete ee\n\nimanya sebagai satu-satunya al-\nternatif. Pride Lands pun jatuh\nke tangan Scar.\n\nSimba, sebaliknya, nyaris ter-\ntelan kebuasan belantara. Un-\ntung, pasangan babi dan kucing,\nPumpaa dan Timon, menolongn-\nya. Dengan bimbingan mereka,\nSimba tumbuh menjadi singa pe-\nmakan serangga. Masa lalu pun\ntenggelam dari ingatannya, sam-\npai muncul Nala, gadi:\nman sepermainan Simba\nkecil.\n\nDari gadis inilah Simba men-\ndengar kesengsaraan yang diala-\nmi rakyat Pride Lands akibat\nkesewenang-wenangan §\nlah Simba bahwa ia me-\nwa ayahnya, ia tak boleh\nmengelak dari tanggung jawab\nyang harus dipikulnya dalam\ndaur kehidupan.\n\nDan, kait-mengait binatang\ndalam rantai makanan yang dis-\nebut daur kehidupan itu memang\nmewarnai seluruh bangunan\nkisah The Lion King. Sebagai raja\nPride Lands, Mufasa sejak dini\n\ntelah mengajarkan daur ke-\nitAcnen banana Simha’ ta +nca\n\n \n\n   \n\n   \n \n\n    \n\nhyena disebut “pemburu-pembu-\nru gelap”, yakni pemakan daging\nyang tersisih dari  rantai\nmakanan. Karena itu, ketika\nScar berkuasa dan memasukkan\nmereka ke dalam daur ke-\nhidupan, keseimbangan dengan\ncepat terganggu.\n\nApalagi, Simba sang putra\nmahkota telah dibuang. Padahal,\ndialah satu-satunya yang bisa\nmenjaga agar hyena-hyena itu\ntetap di luar rantai makanan.\nMaka, hanya ada satu jalan agar\nkeseimbangan pulih, yakni Sim-\nb@harus kembali menempati po-\nmya dan memikul tanggung\njawabnya dalam daur kehidupan. ,\n\nSebagai kartun pertama yang ?\ndibuatnya berdasarkan kisah asli, ®\nDisney tetap menunjukkan kelas-\nnya dalam The Lion King. Tak per-\ncuma Disney memerlukan men-\ngirim tim kreatif ke Afrika Timur\nuntuk melihat langsung ke-\nhidupan binatang-binatang yang\ndimunculkan dalam The Lion\nKing. Lihat, misalnya, betapa lu-\nwes ulah Simba sejak masih boc-\nah singa yang nakal sampai men-\njadi singa dewasa yang keras. Ka-\nlau gda yang bisa dipertanyakan,\nrasanya hanya ini: bagaimana di\nseluruh Pride Lands hanya ada\ntiga singa jantan, yakni Mufasa,\nScar, dan Simba?\n\nNamun, pesona fantastis war-\nna-warni film ini dengan segera\nakan membuat pertanyaan itu\nterluna. Apalagi. The Lion King"
}
```

**NOTE:** The python code example is available here (main.py)