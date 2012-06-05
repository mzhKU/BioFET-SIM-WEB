// Custom formatting of floating point
//function toFixed(value, precision) {
//        var power = Math.pow(10, precision || 0);
//            return String(Math.round(value * power) / power);
//}
function roundit(Num, Places) {
   if (Places > 0) {
      if ((Num.toString().length - Num.toString().lastIndexOf('.')) > (Places + 1)) {
         var Rounder = Math.pow(10, Places);
         return Math.round(Num * Rounder) / Rounder;
      }
      else return Num;
   }
   else return Math.round(Num);
}
