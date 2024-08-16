<%
    # scripts = ['/static/js/home.js']
    title = ''
    page_class = 'home'
%>
% rebase('base.tpl', title = title, page_class = page_class)
<div class="spinner_container">
    <div class="beginning">
        <a href="mailto:hannah.knights@hotmail.co.uk" target="_top">hannah.knights@hotmail.co.uk</a><br>&nbsp;
    </div>
    % for work_html in work_list_html:
        {{!work_html}}
    % end
</div>
<div id="button" class="info">
    *
</div>
<div id="text" class="info hidden">
    Hannah Knights<br>
    based in Sheffield, UK<br>
    <br>
    This site is hand-built, see <a href="https://github.com/HannahKnights/hk-site" target="blank">here</a><br>
    This site has a history, see <a href="https://hannahknights.co.uk/archive/20122017" target="_blank">here</a> (2012 - 2017)<br>
    Other stuff<br>
    Link<br>
    link<br>
</div>
