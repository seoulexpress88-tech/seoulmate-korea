// Travel guides page: filter cards by topic, city and search text, combined. Without JS the chips are plain links.
(function(){
  const finder=document.querySelector(".finder");if(!finder)return;
  const cards=[...document.querySelectorAll(".cards .card")];
  const qs=new URLSearchParams(location.search);
  const state={topic:qs.get("topic"),city:qs.get("city"),q:qs.get("q")||""};
  const search=document.getElementById("guideSearch");search.value=state.q;

  function apply(){
    let n=0;const q=state.q.trim().toLowerCase();
    cards.forEach(c=>{
      const on=(!state.topic||c.dataset.topics.split(" ").includes(state.topic))
        &&(!state.city||c.dataset.cities.split(" ").includes(state.city))
        &&(!q||q.split(/\s+/).every(w=>c.dataset.text.includes(w)));
      c.hidden=!on;if(on)n++;
    });
    const mark=(a,on)=>on?a.setAttribute("aria-current","page"):a.removeAttribute("aria-current");
    finder.querySelectorAll("[data-topic]").forEach(a=>mark(a,a.dataset.topic===state.topic));
    finder.querySelectorAll("[data-city]").forEach(a=>mark(a,a.dataset.city===state.city));
    document.getElementById("guideCount").textContent=`${n} guide${n===1?"":"s"}`+(state.topic||state.city||q?" match":"");
    document.getElementById("guideEmpty").hidden=n>0;
    const p=new URLSearchParams();
    if(state.topic)p.set("topic",state.topic);if(state.city)p.set("city",state.city);if(q)p.set("q",state.q.trim());
    history.replaceState(null,"",location.pathname+(p.toString()?"?"+p:""));
  }
  finder.addEventListener("click",e=>{
    const a=e.target.closest("[data-topic],[data-city]");if(!a)return;
    e.preventDefault();
    if(a.dataset.topic)state.topic=state.topic===a.dataset.topic?null:a.dataset.topic;
    else state.city=state.city===a.dataset.city?null:a.dataset.city;
    apply();
  });
  search.addEventListener("input",()=>{state.q=search.value;apply()});
  document.getElementById("guideReset").addEventListener("click",e=>{
    e.preventDefault();state.topic=state.city=null;state.q="";search.value="";apply();
  });
  apply();
})();
