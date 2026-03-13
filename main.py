from playwright.sync_api import sync_playwright
import json
import time
import os
from datetime import datetime


def scrape_wazone():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu"
            ]
        )

        context = browser.new_context()
        page = context.new_page()

        page.goto("https://wzstats.gg", wait_until="domcontentloaded")

        page.wait_for_selector(".loadout-container")

        armas_finales = []
        armas_vistas = set()

        print("Iniciando scraping dinámico...\n")

        while True:

            items = page.query_selector_all(".loadout-container")

            for current_item in items:

                try:

                    nombre_el = current_item.query_selector(".loadout-content-name")

                    if not nombre_el:
                        continue

                    nombre = nombre_el.inner_text().split("\n")[0].strip()

                    if nombre in armas_vistas:
                        continue

                    armas_vistas.add(nombre)

                    current_item.scroll_into_view_if_needed()

                    time.sleep(0.3)

                    btn = current_item.query_selector(".loadout-action")

                    if btn:
                        page.evaluate("(el)=>el.click()", btn)
                        time.sleep(1)

                    accesorios = list(set([
                        el.inner_text().strip()
                        for el in current_item.query_selector_all(".attachment-name-no-image")
                    ]))

                    code_el = current_item.query_selector(".weapon-build-code")
                    build_code = code_el.inner_text().strip() if code_el else "N/A"

                    img_el = current_item.query_selector("img")
                    img_url = img_el.get_attribute("src") if img_el else "N/A"

                    date_el = current_item.query_selector(".highlight-date")
                    fecha_actualizacion = date_el.inner_text().strip() if date_el else "N/A"

                    rank_el = current_item.query_selector(".loadout-tag.category-position .rank")
                    rank = rank_el.inner_text().strip() if rank_el else "N/A"

                    categoria_el = current_item.query_selector(".loadout-tag.category-position")

                    categoria = "N/A"

                    if categoria_el:
                        categoria = categoria_el.inner_text().replace(rank, "").strip()

                    tipo_el = current_item.query_selector(".loadout-tags .loadout-tag:not(.category-position)")
                    tipo_arma = tipo_el.inner_text().strip() if tipo_el else "N/A"

                    tier = page.evaluate("""
                    (el) => {
                        let parent = el;
                        while(parent){
                            if(parent.previousElementSibling){
                                let prev = parent.previousElementSibling;
                                if(prev.innerText && prev.innerText.match(/Tier/i)){
                                    return prev.innerText.trim();
                                }
                            }
                            parent = parent.parentElement;
                        }
                        return "Unknown";
                    }
                    """, current_item)

                    arma_data = {
                        "nombre": nombre,
                        "tier": tier,
                        "rank": rank,
                        "categoria": categoria,
                        "tipo": tipo_arma,
                        "accesorios": accesorios,
                        "build_code": build_code,
                        "imagen": img_url,
                        "fecha_actualizacion": fecha_actualizacion
                    }

                    armas_finales.append(arma_data)

                    print(f"\nARMA #{len(armas_finales)}")
                    print(json.dumps(arma_data, indent=4, ensure_ascii=False))

                except Exception as e:
                    print("Error:", e)

            page.evaluate("window.scrollBy(0,1500)")
            time.sleep(2)

            footer_visible = page.locator("footer").is_visible()

            if footer_visible:

                page.evaluate("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(4)

                items_check = page.query_selector_all(".loadout-container")

                nombres = [
                    el.query_selector(".loadout-content-name").inner_text().split("\n")[0].strip()
                    for el in items_check
                    if el.query_selector(".loadout-content-name")
                ]

                if all(n in armas_vistas for n in nombres):
                    break

        archivo_json = "data.json"
        backup_folder = "backup"

        os.makedirs(backup_folder, exist_ok=True)

        if os.path.exists(archivo_json):

            fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backup_name = f"{backup_folder}/data_{fecha}.json"

            os.rename(archivo_json, backup_name)

            print(f"\nBackup creado: {backup_name}")

        with open(archivo_json, "w", encoding="utf-8") as f:
            json.dump(armas_finales, f, indent=4, ensure_ascii=False)

        browser.close()

        print("\nSCRAPING COMPLETADO")
        print(f"Total armas guardadas: {len(armas_finales)}")


scrape_wazone()
