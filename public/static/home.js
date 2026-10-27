// Home and destinations page: map pin / chip selects a city panel; month chips filter festivals.
(function(){
  const panels=document.querySelectorAll(".cpanel");
  function select(id){
    if(!document.querySelector(`.cpanel[data-panel="${id}"]`))return;
    panels.forEach(p=>p.hidden=p.dataset.panel!==id);
    document.querySelectorAll(".kmap .pin").forEach(p=>p.classList.toggle("is-active",p.dataset.city===id));
    document.querySelectorAll(".city-chip").forEach(b=>b.setAttribute("aria-pressed",b.dataset.city===id));
  }
  document.querySelectorAll(".kmap a.pin").forEach(a=>{
    a.addEventListener("click",e=>{e.preventDefault();select(a.dataset.city)});
    a.addEventListener("mouseenter",()=>{if(matchMedia("(hover:hover)").matches)select(a.dataset.city)});
    a.addEventListener("focus",()=>select(a.dataset.city));
  });
  document.querySelectorAll(".city-chip").forEach(b=>b.addEventListener("click",()=>select(b.dataset.city)));
  if(panels.length)select("seoul");

  const months=document.querySelectorAll(".months .month");
  if(!months.length)return;
  function showMonth(m){
    months.forEach(b=>b.setAttribute("aria-pressed",+b.dataset.month===m));
    let n=0;
    document.querySelectorAll(".fest-list .fest").forEach(li=>{
      const on=li.dataset.months.split(",").map(Number).includes(m);li.hidden=!on;if(on)n++;
    });
    document.querySelectorAll(".season").forEach(s=>s.hidden=!s.dataset.months.split(",").map(Number).includes(m));
    const empty=document.querySelector(".fest-empty");if(empty)empty.hidden=n>0;
  }
  months.forEach(b=>b.addEventListener("click",()=>showMonth(+b.dataset.month)));
  showMonth(new Date().getMonth()+1);
})();
