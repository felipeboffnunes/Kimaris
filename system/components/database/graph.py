# Python Standard Libraries
import sqlite3
import re
def get_standard_graph():
    try:
        conn = sqlite3.connect("./db/results.db")
        cursor = conn.cursor()

        cursor.execute(f"""
                SELECT article_id, article_title, article_depth, article_cites FROM articles;
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
        
    links = [{"source": 1, "target": 0}, {"source": 4, "target": 2}, {"source": 5, "target": 1},  {"source": 10, "target": 0},\
        {"source": 2, "target": 0}, {"source": 4, "target": 2}, {"source": 5, "target": 1},  {"source": 9, "target": 0},\
            {"source": 3, "target": 0}, {"source": 6, "target": 2}, {"source": 7, "target": 1},  {"source": 8, "target": 0}]
    #for link in links_:
    #    data = {"source": link[0]-1, "target": link[1]-1}
    #    links.append(data)
        
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
            SELECT id, name, depth, cited_by FROM nodes
            WHERE name = "{name}";
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

def create_select_graph_db():
    try:
        new_conn = sqlite3.connect("./db/graph.db")
                
        new_cursor = new_conn.cursor()
        new_cursor.execute("""
        CREATE TABLE nodes (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );             
        """)
        
        new_cursor.execute("""
        CREATE TABLE links (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            source INTEGER NOT NULL,
            target INTEGER NOT NULL
        );             
        """)
    except Exception as e:
        new_cursor.execute("DELETE FROM nodes;")
        new_cursor.execute("DELETE FROM links;")
        
def get_name_by_id(idx):
    print(idx)
    conn = sqlite3.connect("./db/results.db")
    cursor = conn.cursor()
    
    cursor.execute(f"""
    SELECT name FROM nodes
    WHERE id = "{idx}";               
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
            article_depth INTEGER NOT NULL
        );             
        """)
        
        cursor.execute("""
        CREATE TABLE articles_links (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            article_source INTEGER NOT NULL,
            article_target INTEGER NOT NULL
        );             
        """)
    except:
        pass
   
    
   
    for article in articles:
        try:
            article_title = article.bib["title"]
        except:
            article_title = "No title"
        article_title = article_title.replace('"', "'")
        print(article_title)
        
        try:
            article_authors = article.bib["author"]
            article_authors = ",".join(article_authors)
        except:
            article_authors = "No authors"
        print(article_authors)
        
        try:
            article_abstract = article.bib["abstract"]
            article_abstract - "".join(article_abstract)
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
            article_year = "0000"
        print(article_year)
        
              
        article_depth = 1
               
        try:
            cursor.execute(f"""
            INSERT INTO articles (article_title, article_abstract, article_publish_year, article_cites, article_cites_link, article_link, article_depth)
            VALUES ("{article_title}", "{article_abstract}", "{article_year}", "{article_cites}", "{article_cites_link}", "{article_link}", "{article_depth}")              
            """)
            
            conn.commit()
            
        except Exception as e:
            #print(e)
            print(f"Repeated article: {article_title}")
            
        try:
            cursor.execute(f"""
            SELECT article_id FROM articles 
            WHERE article_title = "{article_title}";
            """)
    
            result = cursor.fetchone()
            article_id = result[0]
            
            cursor.execute(f"""
            UPDATE articles
            SET article_depth = "1"
            WHERE article_id = "{article_id}";
            """
            )
        except Exception as e:
            print(e)
            
        print(f"\nArticle: {article_title}\nID: {article_id}\nDepth: {article_depth}")
        def forward(article_id, link, cursor, step=1, total_steps=2):
            print(f"\nStarting forward level {step} for {article_id}")
            if link != "No Citations": 
                cited_by = get_cited_by(link)
                
                
                for cited_article in cited_articles:
                    cited_depth = step
                
                    cited_title = cited_article["bib"]["title"]
                    cited_title = article_title.replace('"', "'")
                    
                    cited_authors = cited_article["bib"]["author"]
                    
                    cited_abstract = cited_article["bib"]["abstract"]
                    cited_abstract - "".join(article_abstract)
                    cited_abstract = article_abstract.replace('"', "'")

                    cited_cites = cited_article["bib"]["cites"]

                    cited_cites_link = cited_article["citations_link"]
                    
                    cited_link = cited_article["bib"]["url"]
                    try:
                        cited_eprint = cited_article["bib"]["eprint"]
                    except:
                        cited_eprint = "None"
                    cited_year = cited_article["bib"]["year"]
                    
                   
                    try:
                        cursor.execute(f"""
                        INSERT INTO nodes (name, article_abstract, article_publish_year, article_cites, article_link, article_cites_link, article_depth)
                        VALUES ("{cited_title}", "{cited_abstract}", "{cited_year}", "{cited_cites}", "{cited_link}", "{cited_cites_link}", "{cited_depth}")              
                        """)
                        
                        conn.commit()
                        
                    except Exception as e:
                        print(f"\n{e}")
                        print(f"Repeated article: {cited_title}")
                    try:
                        cursor.execute(f"""
                        SELECT article_id, article_depth FROM articles 
                        WHERE name = "{cited_title}";
                        """)
                
                        result = cursor.fetchone()
                        cited_id = result[0]
                        
                        aux_cited_depth = result[1]
                        if aux_cited_depth < cited_depth:
                            cursor.execute(f"""
                            UPDATE articles
                            SET group = "{aux_cited_depth}"
                            WHERE id = "{cited_id}";
                            """
                            )
                            
                    except Exception as e:
                        print(e)
                    print(f"\nArticle: {cited_title}\nID: {cited_id} Depth: {cited_depth}")    
                    try:  
                        cursor.execute(f"""
                            INSERT INTO article_links (source, target)
                            VALUES ("{cited_id}", "{article_id}")              
                            """)
                        
                        conn.commit()
                        print(f"\nLink (Source: {cited_id} Target: {article_id})")
                    except Exception as e:
                        print(e)    
                        print(f"\nCouldn't create Link (Source: {cited_id} Target: {article_id})")
                    if total_steps - step > 0:
                        forward(cited_id, cited_cites_link, cursor, step + 1, total_steps)                
            else:
                print("This article was not cited.")
            return
        
        #forward(article_id, article_cites_link, cursor, 2, 3)
        
    conn.commit()
    conn.close()
    
    return