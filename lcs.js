// let a=process.argv.slice(2);a.length<1?console.log(''):(a.sort((a,b)=>a.length-b.length),l='',[s,...o]=a,(()=>{for(let n=s.length;n>0&&!l;n--)for(let i=0;i<=s.length-n;i++)if(o.every(t=>t.includes(s.substr(i,n)))){l=s.substr(i,n);return}})(),console.log(l));

let a = process.argv.slice(2);

a.length < 1 ? console.log('') : (
    a.sort((a, b) => a.length - b.length),
    l = '',
    [s, ...o] = a,
    (() => {
        for (let n = s.length; n > 0 && !l; n--) {
            for (let i = 0; i <= s.length - n; i++) {
                if (o.every(t => t.includes(s.substr(i, n)))) {
                    l = s.substr(i, n);
                    return;
                }
            }
        }
    })(),
    console.log(l)
);
