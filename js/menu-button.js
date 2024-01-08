
    (() =>{
        const menuBtmRef = document.querySelector("[data-menu-button]");
        const mobilMenuRef = document.querySelector("[data-menu]");

        menuBtmRef.addEventListener("click", () =>{
            const expanded = menuBtmRef.getAttribute("aria-expanded") === "true" || false;

            menuBtmRef.setAttribute("aria-expanded", !expanded);
        });
    })();