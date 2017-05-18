sphinx_fe -argfile ./en-us/feat.params -samprate 16000 -c ./data/train-speech.fileids -di ./data/ -do ./data/ -ei wav -eo mfc -mswav yes
cp bw ./data/
cp map_adapt ./data/
cp mk_s2sendump ./data/
cp -r en-us/ ./data/
cd data
./bw -hmmdir en-us -moddeffn en-us/mdef.txt -ts2cbfn .ptm. -feat 1s_c_d_dd -svspec 0-12/13-25/26-38 -cmn current -agc none -dictfn ../../xcopilot/pocketsphinx-data/xp-XP/pronounciation-dictionary.dic -ctlfn train-speech.fileids -lsnfn train-speech.transcription -accumdir .
