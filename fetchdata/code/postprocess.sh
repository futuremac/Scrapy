workdir="/home/q/qiancheng.jiang/appinfo/"
#get comment url
awk -F'\t' '{print $1"\thttp://zhushou.360.cn/detail/index/soft_id/"$1"\t"$8"&appid="$1}' $workdir/data/items.jl > $workdir/data/360.url
