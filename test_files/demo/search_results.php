<!DOCTYPE HTML>
<html>
<head>
    <title>Archives Search</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="styles.css">

</head>
<body>
    <header>
        <h1>Search the Rose Avenue Archives site</h1>
        <nav>
            <a href="https://archives.roseavenue.org">Back to archives website</a>
            <a href="https://roseavenue.org">Visit our Current Website</a>
        </nav>    
    </header>
    <main>
        <section id="search_wrapper">
            <form name="search" action="" method="get">
                <input type="text" name="term" id="search_term" placeholder="Search here">
                <input type='submit' class="active" value="Search">
            </form>
        </section>
        
        <section id="search_results">
            <div id="results_per_page">
                <p>Results per page</p>
                <div id="per_page_buts">
                    <button onclick="setpages('pg_20')" id="but_20" class="res_per active">20</button>
                    <button onclick="setpages('pg_50')" id="but_50" class="res_per">50</button>
                    <button onclick="setpages('pg_100')" id="but_100" class="res_per">100</button>
                </div>
                <div>
                    <button onclick="pagination(-1)" class="but_next" id="prev">&larr;</button>
                    <button onclick="pagination(0)" class="but_next" id="next">&rarr;</button>
                </div>
                <form id="page_log" class="hide">
                    <input type=radio name=per_page value=20 id="pg_20" checked>
                    <input type=radio name=per_page value=50 id="pg_50">
                    <input type=radio name=per_page value=100 id="pg_100">
                </form>
            </div>
            
            <div id="result_wrapper">
<?php 
    if (isset($_GET['term'])) {
        include 'formats.php';
        lookup($_GET['term']);
    } 
?>
            </div>
            <div id="pagination_wrapper">
                
            </div>
        </section>
    </main>
    <footer>
        <div id="reset">
            <form name="reset" action="" method="POST">
                <input type="password" name="passkey" id="passkey" placeholder="PassKey">
                <input type="submit" name="dump" id="reset_index" value="Reset index">
            </form>
        </div>
        <p>Created by <a href="https://moyeraudio.com">MoyerAudio</a> 2021</p>
    </footer>
    <script src="functions.js"></script>
</body>
</html>
<?php 

if ($_POST['passkey']){
    if (password_verify($_POST['passkey'], '$2y$10$NZZBY3sOAjVA9x4k4hjfP.4v9bdDg5CYdPLjXcLfLLvtkw7AdWlFe')){
        include 'crawl.php';
        echo crawl();
    } 
}

?>