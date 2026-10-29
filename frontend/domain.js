/* Shared, independently testable accounting logic. Units: initial NAV = 100. */
(function(root) {
  'use strict';
  function simulate(request, gate, haircut) {
    if (![request,gate,haircut].every(Number.isFinite) || request<0 || request>1 || gate<=0 || gate>1 || haircut<0 || haircut>=1) throw new RangeError('Invalid liquidity assumptions');
    const realization=1-haircut;
    let assets=100,pending=100*request;
    const rows=[];
    while(pending>1e-10&&assets>1e-10){
      const paid=Math.min(pending,100*gate,assets*realization),sold=paid/realization;
      assets=Math.max(0,assets-sold);pending=Math.max(0,pending-paid);
      rows.push({period:rows.length+1,assets,pending,paid,sold,loss:sold-paid});
    }
    return rows;
  }
  if(typeof module!=='undefined'&&module.exports)module.exports={simulate};
  else root.CreditMath={simulate};
})(typeof window!=='undefined'?window:globalThis);
