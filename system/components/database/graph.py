# Python Standard Libraries
import sqlite3
import re
# Manager
from components.manager.search import do_forward_step

def get_author_nodes():
    try:
        conn = sqlite3.connect("./db/results.db")
        cursor = conn.cursor()

        cursor.execute(f"""
                SELECT author_name FROM authors;
                """)

        nodes_ = cursor.fetchall()
        
        cursor.execute(f"""
                    SELECT article_id, article_title, article_depth, article_cites FROM articles; 
                    """)
    
        nodes__ = cursor.fetchall()
        
        cursor.execute(f"""
                SELECT author_source, author_target FROM workedtogether;
                """)
        
        links_ = cursor.fetchall()
        
        cursor.execute(f"""
            SELECT author_id, article_id from wrotepaper;
        """)
        
        links__ = cursor.fetchall()

        
    except Exception as e:
        print(e)
        
    nodes = []
    sizes = []
    for node in nodes__:
        data = {"name": node[1], "group": node[2]}
        nodes.append(data)
        sizes.append(node[3])
    
    
    lenght = len(nodes__)
    for node in nodes_:
        data = {"name": node[0], "group": 5}
        nodes.append(data)
        sizes.append(5)
    
    links = []
    for link in links_:
        data = {"source": link[0]-1, "target": link[1]-1}
        links.append(data)
        
    for link in links__:
        data = {"source": lenght + link[0]-1, "target": link[1]-1}
        links.append(data)
        
    return nodes, links, sizes


def get_standard_graph():
    try:
        conn = sqlite3.connect("./db/results.db")
        cursor = conn.cursor()

        cursor.execute(f"""
                SELECT article_id, article_title, article_depth, article_cites FROM articles;
                """)

        nodes_ = cursor.fetchall()
        
        cursor.execute(f"""
                SELECT article_source, article_target FROM articles_links;
                """)
        
        links_ = cursor.fetchall()
    except Exception as e:
        print(e)
        
    nodes = []
    sizes = []
    for node in nodes_:
        data = {"name": node[1], "group": node[2]}
        nodes.append(data)
        sizes.append(node[3])
    
    links = []
    for link in links_:
        data = {"source": link[0]-1, "target": link[1]-1}
        links.append(data)
        
    return nodes, links, sizes

def get_standard_graph2():
    try:
        conn = sqlite3.connect("./db/results.db")
        cursor = conn.cursor()

        cursor.execute(f"""
                SELECT id, name, depth, cited_by FROM nodes;
                """)

        nodes_ = cursor.fetchall()
        
        cursor.execute(f"""
                SELECT source, target FROM links;
                """)
        
        links_ = cursor.fetchall()
    except Exception as e:
        print(e)
        
    nodes = []
    sizes = []
    for node in nodes_:
        data = {"name": node[1], "group": node[2]}
        nodes.append(data)
        sizes.append(node[3])
        
    links = []
    for link in links_:
        data = {"source": link[0]-1, "target": link[1]-1}
        links.append(data)
        
    return nodes, links, sizes

def get_selected_graph2(name):
    # Name comes parsed from visualization
    name = re.sub("<br>", "", name)
    name = re.sub("(Cited by: \d+)", "", name)
    
    nodes = []
    links = []
    sizes = []
    IDX = 0
    
    create_select_graph_db()
    
    conn = sqlite3.connect("./db/results.db")
    new_conn = sqlite3.connect("./db/graph.db")

    new_cursor = new_conn.cursor()
    cursor = conn.cursor()

    cursor.execute(f"""
            SELECT article_id, article_title, article_depth, article_cites FROM articles
            WHERE article_title = "{name}";
            """)

    node = cursor.fetchone()
    idx = node[0]
    try:
        
        new_cursor.execute(f"""
        INSERT INTO nodes (name)
        VALUES ("{name}")              
        """)
        nodes.append({"name": node[1], "group": node[2]})
        sizes.append(node[3])
        IDX +=1
    except Exception as e:
        print("article 0")

    cursor.execute(f"""
            SELECT source, target FROM links
            WHERE source = "{idx}"
            OR target = "{idx}";
            """)

    links_ = cursor.fetchall()
    for link in links_:
        #links.append({"source": link[0], "target": link[1]})
        if link[0] != idx:
            cursor.execute(f"""
            SELECT id, name, depth, cited_by FROM nodes
            WHERE id = "{link[0]}";
            """)
            node = cursor.fetchone()
            try:
                new_cursor.execute(f"""
                INSERT INTO nodes (name)
                VALUES ("{node[1]}")              
                """)
                nodes.append({"name": node[1], "group": node[2]})
                sizes.append(node[3])
                links.append({"source": IDX, "target": 0})
                if len(links_) == 1:
                    links.append({"source": 0, "target": IDX})
                IDX +=1
                
            except Exception as e:
                print(e)
                try:
                    new_cursor.execute(f"""
                    SELECT id, name FROM nodes
                    WHERE name = "{node[1]}";
                    """)
                    node_id = cursor.fetchone()
                    node_id = node_id[0]
                    nodes.append({"name": node[1], "group": node[2]})
                    sizes.append(node[3])

                    links.append({"source": node_id, "target": 0})
                    if len(links_) == 1:
                        links.append({"source": 0, "target": node_id})
                except:
                    pass
                
        elif link[1] != idx:
            cursor.execute(f"""
            SELECT id, name, depth, cited_by FROM nodes
            WHERE id = "{link[1]}";
            """)
            node = cursor.fetchone()
            try:
                new_cursor.execute(f"""
                INSERT INTO nodes (name)
                VALUES ("{node[1]}");              
                """)
                nodes.append({"name": node[1], "group": node[2]})
                sizes.append(node[3])
                links.append({"source": 0, "target": IDX})
                if len(links_) == 1:
                    links.append({"source": IDX, "target": 0})
                IDX +=1
                
            except Exception as e:
                print(e)
                try:
                    new_cursor.execute(f"""
                    SELECT id, name FROM nodes
                    WHERE name = "{node[1]}";
                    """)
                    node_id = cursor.fetchone()
                    
                    node_id = node_id[0]
                    nodes.append({"name": node[1], "group": node[2]})
                    sizes.append(node[3])

                    links.append({"source": 0, "target": node_id})
                    if len(links_) == 1:
                        links.append({"source": node_id, "target": 0})
                except:
                    pass
        #print(nodes, links)
    return nodes, links, sizes

def delete_node(name):
    # Name comes parsed from visualization
    name = re.sub("<br>", "", name)
    name = re.sub("(Cited by: \d+)", "", name)
    
    conn = sqlite3.connect("./db/results.db")

    cursor = conn.cursor()
    cursor.execute(f"""
            SELECT article_id FROM articles
            WHERE article_title = "{name}";
            """)

    node = cursor.fetchone()
    idx = node[0]
    print(idx)
    
    cursor.execute(f"""
            DELETE FROM articles
            WHERE article_title = "{name}";
            """)
    
    cursor.execute(f"""
            DELETE FROM articles_links
            WHERE article_source = "{idx}"
            OR article_target = "{idx}";
            """)

    cursor.execute(f"""
            SELECT article_target FROM articles_links
            WHERE article_target > "{idx}";       
            """)  
    
    targets = cursor.fetchall()
    for target in targets:
        print(target)
        cursor.execute(f"""
            UPDATE articles_links
            SET article_target = "{target[0] - 1}"
            WHERE article_target = "{target[0]}";
            """)
    
    cursor.execute(f"""
            SELECT article_source FROM articles_links
            WHERE article_source > "{idx}";       
            """)  
    
    sources = cursor.fetchall()
    for source in sources:
        print(source)
        cursor.execute(f"""
            UPDATE articles_links
            SET article_source = "{source[0] - 1}"
            WHERE article_source = "{source[0]}";
            """)
        
    cursor.execute(f"""
            SELECT article_id from articles
            WHERE article_id > "{idx}";       
            """)
    
    articles = cursor.fetchall()
    for article in articles:
        cursor.execute(f"""
                UPDATE articles
                SET article_id = "{article[0] - 1}"
                WHERE article_id = "{article[0]}";
                """)

    conn.commit()
    return None

def get_selected_graph(name):
    # Name comes parsed from visualization
    name = re.sub("<br>", "", name)
    name = re.sub("(Cited by: \d+)", "", name)
    
    nodes = []
    links = []
    sizes = []
    IDX = 0
    
    create_select_graph_db()
    
    conn = sqlite3.connect("./db/results.db")
    new_conn = sqlite3.connect("./db/graph.db")

    new_cursor = new_conn.cursor()
    cursor = conn.cursor()
    cursor.execute(f"""
            SELECT article_id, article_title, article_depth, article_cites FROM articles
            WHERE article_title = "{name}";
            """)

    node = cursor.fetchone()
    idx = node[0]
    try:
        
        new_cursor.execute(f"""
        INSERT INTO articles (article_title)
        VALUES ("{name}")              
        """)
        nodes.append({"name": node[1], "group": node[2]})
        sizes.append(node[3])
        IDX +=1
    except Exception as e:
        print("article 0")

    cursor.execute(f"""
            SELECT article_source, article_target FROM articles_links
            WHERE article_source = "{idx}"
            OR article_target = "{idx}";
            """)

    links_ = cursor.fetchall()
    for link in links_:
        #links.append({"source": link[0], "target": link[1]})
        if link[0] != idx:
            cursor.execute(f"""
            SELECT article_id, article_title, article_depth, article_cites FROM articles
            WHERE article_id = "{link[0]}";
            """)
            node = cursor.fetchone()
            try:
                new_cursor.execute(f"""
                INSERT INTO articles (article_title)
                VALUES ("{node[1]}")              
                """)
                nodes.append({"name": node[1], "group": node[2]})
                sizes.append(node[3])
                links.append({"source": IDX, "target": 0})
                if len(links_) == 1:
                    links.append({"source": 0, "target": IDX})
                IDX +=1
                
            except Exception as e:
                print(e)
                try:
                    new_cursor.execute(f"""
                    SELECT article_id, article_title FROM articles
                    WHERE article_title = "{node[1]}";
                    """)
                    node_id = cursor.fetchone()
                    node_id = node_id[0]
                    nodes.append({"name": node[1], "group": node[2]})
                    sizes.append(node[3])

                    links.append({"source": node_id, "target": 0})
                    if len(links_) == 1:
                        links.append({"source": 0, "target": node_id})
                except:
                    pass
                
        elif link[1] != idx:
            cursor.execute(f"""
            SELECT article_id, article_title, article_depth, article_cites FROM articles
            WHERE article_id = "{link[1]}";
            """)
            node = cursor.fetchone()
            try:
                new_cursor.execute(f"""
                INSERT INTO articles (article_title)
                VALUES ("{node[1]}");              
                """)
                nodes.append({"name": node[1], "group": node[2]})
                sizes.append(node[3])
                links.append({"source": 0, "target": IDX})
                if len(links_) == 1:
                    links.append({"source": IDX, "target": 0})
                IDX +=1
                
            except Exception as e:
                print(e)
                try:
                    new_cursor.execute(f"""
                    SELECT article_id, article_title FROM articles
                    WHERE article_title = "{node[1]}";
                    """)
                    node_id = cursor.fetchone()
                    
                    node_id = node_id[0]
                    nodes.append({"name": node[1], "group": node[2]})
                    sizes.append(node[3])

                    links.append({"source": 0, "target": node_id})
                    if len(links_) == 1:
                        links.append({"source": node_id, "target": 0})
                except:
                    pass
        #print(nodes, links)
    return nodes, links, sizes

def create_select_graph_db():
    try:
        new_conn = sqlite3.connect("./db/graph.db")
                
        new_cursor = new_conn.cursor()
        new_cursor.execute("""
        CREATE TABLE articles (
            article_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            article_title TEXT UNIQUE NOT NULL
        );             
        """)
        
        new_cursor.execute("""
        CREATE TABLE articles_links (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            article_source INTEGER NOT NULL,
            article_target INTEGER NOT NULL
        );             
        """)
    except Exception as e:
        new_cursor.execute("DELETE FROM articles;")
        new_cursor.execute("DELETE FROM articles_links;")
        
def get_name_by_id(idx):
    print(idx)
    conn = sqlite3.connect("./db/results.db")
    cursor = conn.cursor()
    
    cursor.execute(f"""
    SELECT article_title FROM articles
    WHERE article_id = "{idx}";               
    """)
    
    result = cursor.fetchone()
    
    print(result)
    name = result[0]
    
    return name


def populate_database(articles, name="results", levels=1):

    database_name = f"{name}.db"
    conn = sqlite3.connect(database_name)
    
    cursor = conn.cursor()
    try:
        cursor.execute("""
        CREATE TABLE articles (
            article_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            article_title TEXT UNIQUE NOT NULL,
            article_abstract TEXT NOT NULL,
            article_publish_year INTEGER NOT NULL,
            article_cites INTEGER NOT NULL,
            article_cites_link TEXT,
            article_link TEXT,
            article_depth INTEGER NOT NULL,
            article_authors TEXT NOT NULL
        );             
        """)
        
        cursor.execute("""
        CREATE TABLE articles_links (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            article_source INTEGER NOT NULL,
            article_target INTEGER NOT NULL
        );             
        """)
        
        cursor.execute("""
        CREATE TABLE authors (
            author_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            author_name TEXT UNIQUE NOT NULL
        );
        """)
        
        cursor.execute("""
        CREATE TABLE workedtogether (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            author_source INTEGER NOT NULL,
            author_target INTEGER NOT NULL
        );          
        """)
        
        cursor.execute("""
        CREATE TABLE wrotepaper (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            author_id INTEGER NOT NULL,
            article_id INTEGER NOT NULL 
        );               
        """)
        
        
        conn.commit()
        
    except Exception as e:
        print(e)
        print("didnt create tables")
        
   
    
   
    for article in articles:
        try:
            article_title = article.bib["title"]
        except:
            article_title = "No title"
        article_title = article_title.replace('"', "'")
        print(article_title)
        
        try:
            article_authors = article.bib["author"]
            if isinstance(article_authors, list):
                article_authors = " and ".join(article_authors)
        except:
            article_authors = "No authors"
        print(article_authors)
        
        try:
            article_abstract = article.bib["abstract"]
            #article_abstract - "".join(article_abstract)
        except:
            article_abstract = "No abstract"
        article_abstract = article_abstract.replace('"', "'")
        print(article_abstract)

        try:
            article_cites = article.bib["cites"]
        except:
            article_cites = "No citations"
        print(article_cites)

        try:
            article_cites_link = article.citations_link
        except:
            article_cites_link = "No cites link" 
        print(article_cites_link)
        
        try:
            article_link = article.bib["url"]
        except:
            article_link = "No link"
        print(article_link)
        
        try:
            article_eprint = article.bib["eprint"]
        except:
            article_eprint = "None"
            
        try:
            article_year = article.bib["year"]
        except:
            article_year = "0"
        print(article_year)
        
              
        article_depth = 0
               
        try:
            cursor.execute(f"""
            INSERT INTO articles (article_title, article_abstract, article_publish_year, article_cites, article_cites_link, article_link, article_depth, article_authors)
            VALUES ("{article_title}", "{article_abstract}", "{article_year}", "{article_cites}", "{article_cites_link}", "{article_link}", "{article_depth}", "{article_authors}")              
            """)
            
            conn.commit()
            
        except Exception as e:
            print(e)
            print(f"Repeated article: {article_title}")
        article_id = ""   
        try:
            cursor.execute(f"""
            SELECT article_id FROM articles 
            WHERE article_title = "{article_title}";
            """)
    
            result = cursor.fetchone()
            article_id = result[0]
        except Exception as e:
            print(e)
            print("didnt find article")
        try:
            cursor.execute(f"""
            UPDATE articles
            SET article_depth = "0"
            WHERE article_id = "{article_id}";
            """
            )
        except Exception as e:
            print(e)
        
        author_names = article_authors.split(" and ")
        for author_name in author_names:
            try:
                cursor.execute(f"""
                INSERT INTO authors (author_name)
                VALUES ("{author_name}")
                """)
            except Exception as e:
                print(e)
                print("repeated author")
        
        for i, author_name in enumerate(author_names):   
            try:     
                cursor.execute(f"""
                SELECT author_id FROM authors 
                WHERE author_name = "{author_name}";
                """)
        
                result = cursor.fetchone()
                author_id = result[0]
                
                cursor.execute(f"""
                INSERT INTO wrotepaper (author_id, article_id)
                VALUES ("{author_id}", "{article_id}")               
                """)
            except Exception as e:
                print(e)
                print("didnt find author or article")
                
            for z, author_name_ in enumerate(author_names):
                if z != i:
                    try:
                        cursor.execute(f"""
                        SELECT author_id from authors
                        WHERE author_name = "{author_name_}" 
                        """)

                        result = cursor.fetchone()
                        author_id_ = result[0]
                        
                        cursor.execute(f"""
                        INSERT INTO workedtogether (author_source, author_target)
                        VALUES ("{author_id}", "{author_id_}")               
                        """)
                    except Exception as e:
                        print(e)
                        print("didnt find both authors")
            
                
                
                
            
        print(f"\nArticle: {article_title}\nID: {article_id}\nDepth: {article_depth}")
        def forward(article, article_id, cursor, step=1, total_steps=2):
            print(f"\nStarting forward level {step} for {article_id}")
            cited_articles = do_forward_step(article)
            if cited_articles != []: 
                for cited_article in cited_articles:
                    try:
                        cited_article_title = cited_article.bib["title"]
                    except:
                        cited_article_title = "No title"
                    cited_article_title = cited_article_title.replace('"', "'")
                    print(cited_article_title)
                    
                    try:
                        cited_article_authors = cited_article.bib["author"]
                        if isinstance(cited_article_authors, list):
                            cited_article_authors = " and ".join(cited_article_authors)
                    except:
                        cited_article_authors = "No authors"
                    print(cited_article_authors)
                    
                    try:
                        cited_article_abstract = cited_article.bib["abstract"]
                        #article_abstract - "".join(article_abstract)
                    except:
                        cited_article_abstract = "No abstract"
                    cited_article_abstract = cited_article_abstract.replace('"', "'")
                    print(cited_article_abstract)

                    try:
                        cited_article_cites = cited_article.bib["cites"]
                    except:
                        cited_article_cites = "No citations"
                    print(cited_article_cites)

                    try:
                        cited_article_cites_link = cited_article.citations_link
                    except:
                        cited_article_cites_link = "No cites link" 
                    print(cited_article_cites_link)
                    
                    try:
                        cited_article_link = cited_article.bib["url"]
                    except:
                        cited_article_link = "No link"
                    print(cited_article_link)
                    
                    try:
                        cited_article_eprint = cited_article.bib["eprint"]
                    except:
                        cited_article_eprint = "None"
                        
                    try:
                        cited_article_year = cited_article.bib["year"]
                    except:
                        cited_article_year = "0"
                    print(cited_article_year)
                    
                        
                    cited_article_depth = step
                    
                
                    try:
                        cursor.execute(f"""
                        INSERT INTO articles (article_title, article_abstract, article_publish_year, article_cites, article_cites_link, article_link, article_depth, article_authors)
                        VALUES ("{cited_article_title}", "{cited_article_abstract}", "{cited_article_year}", "{cited_article_cites}", "{cited_article_cites_link}", "{cited_article_link}", "{cited_article_depth}", "{cited_article_authors}")              
                        """)
                        
                        conn.commit()
                        
                    except Exception as e:
                        print(f"\n{e}")
                        print(f"Repeated article: {cited_article_title}")
                    try:
                        cursor.execute(f"""
                        SELECT article_id, article_depth FROM articles 
                        WHERE article_title = "{cited_article_title}";
                        """)
                
                        result = cursor.fetchone()
                        cited_article_id = result[0]
                        
                        aux_cited_depth = result[1]
                        if aux_cited_depth < cited_article_depth:
                            cursor.execute(f"""
                            UPDATE articles
                            SET article_depth = "{aux_cited_depth}"
                            WHERE article_id = "{cited_article_id}";
                            """
                            )
                            
                    except Exception as e:
                        print(e)
                        
                    author_names = cited_article_authors.split(" and ")
                    for author_name in author_names:
                        try:
                            cursor.execute(f"""
                            INSERT INTO authors (author_name)
                            VALUES ("{author_name}")
                            """)
                        except Exception as e:
                            print(e)
                            print("repeated author")
                    
                    for i, author_name in enumerate(author_names):   
                        try:     
                            cursor.execute(f"""
                            SELECT author_id FROM authors 
                            WHERE author_name = "{author_name}";
                            """)
                    
                            result = cursor.fetchone()
                            author_id = result[0]
                            
                            cursor.execute(f"""
                            INSERT INTO wrotepaper (author_id, article_id)
                            VALUES ("{author_id}", "{cited_article_id}")               
                            """)
                        except Exception as e:
                            print(e)
                            print("didnt find author or article")
                            
                        for z, author_name_ in enumerate(author_names):
                            if z != i:
                                try:
                                    cursor.execute(f"""
                                    SELECT author_id from authors
                                    WHERE author_name = "{author_name_}" 
                                    """)

                                    result = cursor.fetchone()
                                    author_id_ = result[0]
                                    
                                    cursor.execute(f"""
                                    INSERT INTO workedtogether (author_source, author_target)
                                    VALUES ("{author_id}", "{author_id_}")               
                                    """)
                                except Exception as e:
                                    print(e)
                                    print("didnt find both authors")        
                        
                
                    print(f"\nArticle: {cited_article_title}\nID: {cited_article_id} Depth: {cited_article_depth}")    
                    try:  
                        cursor.execute(f"""
                            INSERT INTO articles_links (article_source, article_target)
                            VALUES ("{cited_article_id}", "{article_id}")              
                            """)
                        
                        conn.commit()
                        print(f"\nLink (Source: {cited_article_id} Target: {article_id})")
                    except Exception as e:
                        print(e)    
                        print(f"\nCouldn't create Link (Source: {cited_article_id} Target: {article_id})")
                    if total_steps - step > 0:
                        forward(cited_article, cited_article_id, cursor, step + 1, total_steps)                
            else:
                print("This article was not cited.")
            return
        
        forward(article, article_id, cursor, 1, 1)
        
    conn.commit()
    conn.close()
    
    return