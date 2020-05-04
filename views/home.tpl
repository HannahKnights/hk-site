<%
    # scripts = ['/static/js/home.js']
    title = ''
    page_class = 'home'

    print(work_list_html)

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
