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

$(document).ready(function()
{
    // Constants, all SI
    var piPower4over3   =  Math.pow(3.141592653589793, 4/3.0);
    var hbarSquared     =          (1.054571628E-34)*(1.054571628E-34)
    var elChargeSquared =          (1.602176487E-19)*(1.602176487E-19);
    var electron_mass   =           9.10938215e-31;
    var eps0            =           8.854187817e-12;

    // Comes in as nm
    function get_np0(ltf)
    {
        var meff               = $('#meff').val()*electron_mass;
        var eps1               = $('#eps1').val()*eps0; 

        // Convert l_TF from nm to meters then square
        var lTFInMetersSquared = Math.pow(ltf*1E-9, 2); 
        var numerator          = hbarSquared*eps1*piPower4over3;
        var denominator        = meff*elChargeSquared*lTFInMetersSquared;

        // Convert m^{-3} to cm^{-3}
        //var np0                = (Math.pow( numerator/denominator, 3)*1E-6).toExponential(3)
        
        // No conversion
        var np0                = (Math.pow( numerator/denominator, 3)).toExponential(3)
        $('#np0').val(np0);
    }

    // Comes in as meter qube
    function get_ltf(np0)
    {
        var meff        = $('#meff').val()*electron_mass;
        var eps1        = $('#eps1').val()*eps0; 
        var numerator   = hbarSquared*eps1*piPower4over3;

        // Working with m^{-3}
        var denominator = meff*elChargeSquared*Math.pow(np0, 1.0/3.0);

        // Converting from cm^{-3} to m^{-3}
        //var denominator = meff*elChargeSquared*Math.pow(np0*1E6, 1.0/3.0);

        // Convert from meter to nm and display two decimal digits
        var lTF         = roundit(Math.sqrt(numerator/denominator)*1E9, 2).toPrecision(3);
        $('#ltf').val(lTF);
    }

    $('#ltf').keyup(function()
    {
        var ltf = $(this).val();
        get_np0(ltf);
    }); // end tf keyup

    $('#np0').keyup(function()
    {
        var np0 = $(this).val();
        get_ltf(np0);
    }); // end np0 keyup

    $('#meff').keyup(function()
    {
        var meff = $(this).val();
        var ltf  = $('#ltf').val();
        get_np0(ltf);
    }); // end meff keyup

    $('#eps1').keyup(function()
    {
        var eps1 = $(this).val();
        var ltf = $('#ltf').val();
        get_np0(ltf);
    }); // end eps1 keyup
}); // end ready
