/*
    ============================================================
    Utils
    Designed and developed by Barrows
    http://www.barrowsonline.com/
    Author: Daniel Carvalho
    ============================================================
*/
(
    function( $ )
    {
		$.fn.exists = function()
		{
			var exists = false;
			
			if (this.length > 0)
			{
				exists = true;
			}
			
			return exists;
		}
    }
)
(jQuery);