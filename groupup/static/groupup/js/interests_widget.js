const createInterestsWidget = (id) => {
    let dropdown = document.querySelector(`select#${id}`);
    const input = document.querySelector("input#interest-select-filter");
    const selectedItems = document.querySelector("div.selected-items");
    let dropdownFlyout = document.querySelector("div.form-select-flyout");
    let dropdownItems = document.querySelector("div#interest-select-items");
    let dropdownOverlay = document.querySelector(".form-select-dismiss-overlay");

    dropdown.addEventListener("mousedown", e => {
        e.preventDefault();
    });

    input.addEventListener("input", e => {
        for (const button of dropdownItems.children) {
            if (button.innerText.toLowerCase().startsWith(input.value) || input.value === "") {
                button.classList.remove("filtered");
            }
            else {
                button.classList.add("filtered");
            }
        }
    })

    const createButton = (option, index) => {
        const button = document.createElement("button");

        const content = document.createElement("span");
        content.classList.add("content");
        content.innerText = option.innerText;
        button.appendChild(content);

        const icon = document.createElement("span");
        icon.classList.add("icon");
        icon.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" data-supported-dps="16x16" fill="currentColor" class="mercado-match" width="16" height="16" focusable="false">
            <path d="M12.57 2H15L6 15l-5-5 1.41-1.41 3.31 3.3z"></path>
        </svg>`;
        button.appendChild(icon);

        button.attributes["item-index"] = index;
        button.classList.add("dropdown-option");
        dropdownItems.appendChild(button);
        return button;
    }

    const onOptionClicked = (option, e) => {
        e.preventDefault();
        option.toggleAttribute("selected");
        const button = e.currentTarget;
        button.toggleAttribute("selected");
        if (button.hasAttribute("selected")) {
            selectedItems.appendChild(button);
        }
        else {
            const index = parseInt(button.attributes["item-index"]);
            dropdownItems.insertBefore(button, dropdownItems.children[index]);
        }
        dismiss();
    }

    for (let i = 0; i < dropdown.options.length; i++) {
        const option = dropdown.options[i];
        const button = createButton(option, i);
        button.addEventListener("click", e => onOptionClicked(option, e));
    }

    input.addEventListener("focus", e => {
        e.preventDefault();
        if (dropdownFlyout.classList.contains("active")) {
            return;
        }

        dropdownFlyout.classList.add("active");
        dropdownFlyout.addEventListener("focusout", e => {
            if (!dropdownFlyout.contains(e.relatedTarget)) {
                dismiss();
            }
        });
        dropdownOverlay.addEventListener("click", e => {
            dismiss();
        })
    });

    dropdown.addEventListener("click", e => {
        e.preventDefault();
        const isActive = dropdownFlyout.classList.contains("active");
        if (isActive) {
            return;
        }

        dropdownFlyout.classList.add("active");
        dropdownOverlay.addEventListener("click", e => {
            dismiss();
        })
    });

    const dismiss = () => {
        dropdownFlyout.classList.remove("active");
        input.value = "";
        for (const b of dropdownItems.children) {
            b.classList.remove("filtered");
        }
    }
}