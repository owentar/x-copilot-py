rm -fr ./data/en-us
rm -fr ./data/en-us-adapt
sphinx_fe -argfile ./en-us/feat.params -samprate 16000 -c ./data/train-speech.fileids -di ./data/ -do ./data/ -ei wav -eo mfc -mswav yes
cp bw ./data/
cp map_adapt ./data/
cp mk_s2sendump ./data/
cp -r en-us/ ./data/
cd data
./bw -hmmdir en-us -moddeffn en-us/mdef.txt -ts2cbfn .ptm. -feat 1s_c_d_dd -svspec 0-12/13-25/26-38 -cmn current -agc none -dictfn ../../xcopilot/pocketsphinx-data/xp-XP/pronounciation-dictionary.dic -ctlfn train-speech.fileids -lsnfn train-speech.transcription -accumdir .
cp -a en-us en-us-adapt
./map_adapt \
    -moddeffn en-us/mdef.txt \
    -ts2cbfn .ptm. \
    -meanfn en-us/means \
    -varfn en-us/variances \
    -mixwfn en-us/mixture_weights \
    -tmatfn en-us/transition_matrices \
    -accumdir . \
    -mapmeanfn en-us-adapt/means \
    -mapvarfn en-us-adapt/variances \
    -mapmixwfn en-us-adapt/mixture_weights \
    -maptmatfn en-us-adapt/transition_matrices
./mk_s2sendump \
    -pocketsphinx yes \
    -moddeffn en-us-adapt/mdef.txt \
    -mixwfn en-us-adapt/mixture_weights \
    -sendumpfn en-us-adapt/sendump
rm en-us-adapt/mixture_weights
rm en-us-adapt/mdef.txt
cp -fr en-us-adapt/. ../../xcopilot/pocketsphinx-data/xp-XP/acoustic-model
