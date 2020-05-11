<%
    page_class = '%s-page' % page_class if page_class else ''
%>
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>

        <meta name="description" content="website, 2017 - ongoing. website, 2012 - 2017 http://20122017.hannahknights.co.uk" />
        <meta name="keywords" content="contemporary, art, artist, hannah, knights, s1artspace, edinburgh college of art, eca, london, sheffield" />

        % if defined('styles'):
            % styles = styles if styles and type(styles) == list else []
            % for style in styles:
                <link href="{{ style }}" rel="stylesheet" type="text/css">
            % end
        % end
        <link href="/static/style/base.css" rel="stylesheet" type="text/css">
        <script src="https://code.jquery.com/jquery-3.1.0.min.js"></script>
        <script src="/static/js/shared.js"></script>
        % if defined('scripts'):
            % scripts = scripts if scripts and type(scripts) == list else []
            % for script in scripts:
                <script src="{{ script }}"></script>
            % end
        % end
        <meta name="viewport" content="width=device-width, initial-scale=0.9">
        <title>Hannah Knights{{' | %s' % title if title else ''}}</title>

    </head>
    <body class='{{page_class}}'>
        <div id='content'>
            {{!base}}
        </div>
    </body>
</html>
