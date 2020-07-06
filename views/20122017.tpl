<%

    is_cv = True if is_cv else False
    print(is_cv)

%>
<html>
  <head>

    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /><meta name="keywords" content="contemporary, art, artist, hannah, knights, s1artspace" />
    <title>hannahknights.co.uk</title>
    <link href="/static/style/archive/20122017/base.css" rel="stylesheet" type="text/css" />

  </head>
  <body>

    % if is_cv:

        <div id="cv">
            <p>
            hannah.knights@hotmail.co.uk<br />
            <br />
            b. 1989<br />
            Lives and works in London.
            <br/>
            <br />
            Studio holder at <a href="http://www.s1artspace.org">S1 Artspace</a> (2011-2013)
            <br />
            Studied at Edinburgh College of Art (2007-2011)<br /><br />
            <br />
            <div id="back"><a href="/archive/20122017" class="blank"> <p2> < back </p2></a></div>
        </div>

    % else:

        <div id="mask"></div>

        <img src="/static/images/archive/20122017/page-4-V2.png" class="workLayout" data="3" />
        <img src="/static/images/archive/20122017/page-2-V3.png" class="workLayout" data="1" />
        <img src="/static/images/archive/20122017/page-1-V3.png" class="workLayout" data="2" />
        <img src="/static/images/archive/20122017/page-3-V3.png" class="workLayout" data="4" />

        <table>
          <tr id="top">
            <td class="left">
              <div class='shutLinks'>
                <a class="shut">close</a> / <a class="shut" data='all'>clear all</a>
              </div>
            </td>
            <td class="center">
              <a class="open" data='1' >click for work</a>
            </td>
            <td class="right"></td>
          </tr>
          <tr id="middle">
            <td class="left">
              <a class="open" data='2' >& more</a>
            </td>
            <td class="center"></td>
            <td class="right">
              <a class="open" data='4' >& more</a>
            </td>
          </tr>
          <tr id="bottom">
            <td class="left"></td>
            <td class="center">
              <a class="open" data='3'>click for more work</a>
            </td>
            <td class="right"></td>
          </tr>
        </table>

        <table id="title">
          <tr id="main">
            <td class="center">
              Hannah Knights<br/>
              <a href="/archive/20122017/cv" class="info">( info )</a>
            </td>
          </tr>
        </table>

    % end

    <script src="https://code.jquery.com/jquery-3.1.0.min.js"></script>
    <script>


      function hover() {
        $('a.info').addClass('hover')
      }

      function unhover() {
        $('a.info').removeClass('hover')
      }

      function openLink() {
        window.open( $('a.info').attr('href') , '_self')
      }

      function openWorkLayout() {
        var imgNum = $(this).attr('data')
        var workLayout = $('img[data="' + imgNum + '"]')
        if (workLayout) {
          var openImg = $('img:visible')
          var zIndex = 2
          if (openImg) {
            openImg.each( function() {
              if ( $(this).css('z-index') >= zIndex ) {
                zIndex = zIndex + 1
              }
            })
          }
          $('div.shutLinks').show()
          workLayout.css('z-index', zIndex)
          workLayout.show()
          $('table a.shut').first().attr('data', imgNum)
        }
      }

      function closeWorkLayout() {
        if ( $(this).attr('data') == 'all' ) {
          closeAll()
        }
        else {
          var img = $(this).attr('data')
          $('img[data="' + img +'"]').hide()
          updateLinkData()
          if ( ! $('img:visible').length ) {
            $('div.shutLinks').hide()
          }
        }
      }

      function closeAll() {
        $('img').hide()
        $('div.shutLinks').hide()
      }

      function updateLinkData() {
        var imgNum = ''
        var closeImgLink = $('table a.shut').first()
        var openImg = $('img:visible')
        if (openImg.length > 1) {
          counter = 0
          openImg.each( function() {
            zIndex = 0
            currentZ = $(this).css('z-index')
            if (currentZ > zIndex) {
              zIndex = currentZ
              imgNum = $(this).attr('data')
            }
          })
        }
        else {
          var imgNum = openImg.first().attr('data')
        }
        closeImgLink.attr( 'data', imgNum )
      }

      $(document).ready( function() {

        var mask = $('#mask')
        var workLink = $('table a.open')
        var closeLink = $('table a.shut')

        mask.mouseenter( hover )

        mask.mouseleave( unhover )

        mask.click( openLink )

        workLink.click( openWorkLayout )

        closeLink.click( closeWorkLayout )



      })

    </script>
  </body>
</html>
