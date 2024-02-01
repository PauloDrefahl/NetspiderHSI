'use strict'; 
var aria = aria || {}; 
const vs = require('fs');


document.addEventListener("DOMContentLoaded", function () {
    var settingsLink = document.getElementById("settings-link");
    var netspiderLink = document.getElementById("netspider-link");
    var boxes = document.querySelectorAll(".box");
    var bigBox = document.getElementById("big-box");

    settingsLink.addEventListener("click", function () {
        // Trigger hover effect on the three boxes
        boxes.forEach(function (box) {
            box.classList.add("hover-effect");
        });

        setTimeout(function () {
            boxes.forEach(function (box) {
                box.classList.remove("hover-effect");
            });
        }, 1000);
    });

    netspiderLink.addEventListener("click", function () {
        // Trigger hover effect on the big box
        bigBox.classList.add("hover-effect");

        setTimeout(function () {
            bigBox.classList.remove("hover-effect");
        }, 1000);
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const fileInputs = document.querySelectorAll('.file-input');

    fileInputs.forEach(input => {
        input.addEventListener('change', function () {
            if (this.files.length > 0) {
                this.classList.add('file-selected');
            } else {
                this.classList.remove('file-selected');
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    var selectAllButton = document.getElementById("select-all-btn");
    var listbox = document.getElementById("ss_elem_list");
  
    selectAllButton.addEventListener("click", function () {
        var items = listbox.querySelectorAll('[role="option"]');
        var isNotSelected = selectAllButton.classList.contains("clicked");
    
        if (isNotSelected) {
            // Select all items
            items.forEach(function (item) {
                item.setAttribute("aria-selected", "true");
                item.classList.remove("selected");
                item.style.backgroundColor = '#09558B'; // Reset background color
                item.style.color = 'white'; // Reset text color
            });
        } else {
            // Deselect all items
            items.forEach(function (item) {
                item.setAttribute("aria-selected", "true");
                item.classList.add("selected");
                item.style.backgroundColor = 'white'; 
                item.style.color = 'black'; 
            });
        }
    });
});

aria.Listbox = class Listbox {
    constructor(listboxNode) {
        this.listboxNode = listboxNode;
        this.activeDescendant = this.listboxNode.getAttribute('aria-activedescendant');
        this.multiselectable = true; // Update to allow multiple selection
        this.moveUpDownEnabled = false;
        this.siblingList = null;
        this.startRangeIndex = 0;
        this.upButton = null;
        this.downButton = null;
        this.moveButton = null;
        this.keysSoFar = '';
        this.handleFocusChange = function () {};
        this.handleItemChange = function () {};
        this.registerEvents();
      }
    /* Initialize the listbox */ 
    registerEvents() {
      this.listboxNode.addEventListener('focus', this.setupFocus.bind(this));
      this.listboxNode.addEventListener('keydown', this.checkKeyPress.bind(this));
      this.listboxNode.addEventListener('click', this.checkClickItem.bind(this));
      this.listboxNode.addEventListener('dblclick', this.handleDoubleClick.bind(this));
  
      if (this.multiselectable) {
        this.listboxNode.addEventListener(
          'mousedown',
          this.checkMouseDown.bind(this)
        );
      }
    }

    /* When the listbox receives focus, set the focus to the previously active descendant, or the first option */
    setupFocus() {
      if (this.activeDescendant) {
        const listitem = document.getElementById(this.activeDescendant);
        listitem.scrollIntoView({ block: 'nearest', inline: 'nearest' });
      }
    }

    /* Handle key presses from the user */
    focusFirstItem() {
      var firstItem = this.listboxNode.querySelector('[role="option"]');
  
      if (firstItem) {
        this.focusItem(firstItem);
      }
    }

    /* Focus on the last option */
    focusLastItem() {
      const itemList = this.listboxNode.querySelectorAll('[role="option"]');
  
      if (itemList.length) {
        this.focusItem(itemList[itemList.length - 1]);
      }
    }

    handleDoubleClick(evt) {
        if (evt.target.getAttribute('role') === 'option') {
            const doubleClickedItem = evt.target;
            const isYellow = doubleClickedItem.classList.contains('yellow-background');
            
            if (isYellow) {
                // Remove yellow background color on double-click
                doubleClickedItem.classList.remove('yellow-background');
                doubleClickedItem.style.backgroundColor = ''; // Reset background color
            } else {
                // Toggle yellow background color on double-click
                doubleClickedItem.classList.add('yellow-background');
                doubleClickedItem.style.backgroundColor = 'yellow'; // Set background color to yellow
            }
        }
    }

    /* Focus on the next option */
    checkKeyPress(evt) {
      const lastActiveId = this.activeDescendant;
      const allOptions = this.listboxNode.querySelectorAll('[role="option"]');
      const currentItem =
        document.getElementById(this.activeDescendant) || allOptions[0];
      let nextItem = currentItem;
  
      if (!currentItem) {
        return;
      }
  
      switch (evt.key) {
        case 'PageUp':
        case 'PageDown':
          evt.preventDefault();
          if (this.moveUpDownEnabled) {
            if (evt.key === 'PageUp') {
              this.moveUpItems();
            } else {
              this.moveDownItems();
            }
          }
  
          break;
        case 'ArrowUp':
        case 'ArrowDown':
          evt.preventDefault();
          if (!this.activeDescendant) {
            // focus first option if no option was previously focused, and perform no other actions
            this.focusItem(currentItem);
            break;
          }
  
          if (this.moveUpDownEnabled && evt.altKey) {
            evt.preventDefault();
            if (evt.key === 'ArrowUp') {
              this.moveUpItems();
            } else {
              this.moveDownItems();
            }
            this.updateScroll();
            return;
          }
  
          if (evt.key === 'ArrowUp') {
            nextItem = this.findPreviousOption(currentItem);
          } else {
            nextItem = this.findNextOption(currentItem);
          }
  
          if (nextItem && this.multiselectable && event.shiftKey) {
            this.selectRange(this.startRangeIndex, nextItem);
          }
  
          if (nextItem) {
            this.focusItem(nextItem);
          }
  
          break;
  
        case 'Home':
          evt.preventDefault();
          this.focusFirstItem();
  
          if (this.multiselectable && evt.shiftKey && evt.ctrlKey) {
            this.selectRange(this.startRangeIndex, 0);
          }
          break;
  
        case 'End':
          evt.preventDefault();
          this.focusLastItem();
  
          if (this.multiselectable && evt.shiftKey && evt.ctrlKey) {
            this.selectRange(this.startRangeIndex, allOptions.length - 1);
          }
          break;
  
        case 'Shift':
          this.startRangeIndex = this.getElementIndex(currentItem, allOptions);
          break;
  
        case ' ':
          evt.preventDefault();
          this.toggleSelectItem(nextItem);
          break;
  
        case 'Backspace':
        case 'Delete':
        case 'Enter':
          if (!this.moveButton) {
            return;
          }
  
          var keyshortcuts = this.moveButton.getAttribute('aria-keyshortcuts');
          if (evt.key === 'Enter' && keyshortcuts.indexOf('Enter') === -1) {
            return;
          }
          if (
            (evt.key === 'Backspace' || evt.key === 'Delete') &&
            keyshortcuts.indexOf('Delete') === -1
          ) {
            return;
          }
  
          evt.preventDefault();
  
          var nextUnselected = nextItem.nextElementSibling;
          while (nextUnselected) {
            if (nextUnselected.getAttribute('aria-selected') != 'true') {
              break;
            }
            nextUnselected = nextUnselected.nextElementSibling;
          }
          if (!nextUnselected) {
            nextUnselected = nextItem.previousElementSibling;
            while (nextUnselected) {
              if (nextUnselected.getAttribute('aria-selected') != 'true') {
                break;
              }
              nextUnselected = nextUnselected.previousElementSibling;
            }
          }
  
          this.moveItems();
  
          if (!this.activeDescendant && nextUnselected) {
            this.focusItem(nextUnselected);
          }
          break;
  
        case 'A':
        case 'a':
          // handle control + A
          if (evt.ctrlKey || evt.metaKey) {
            if (this.multiselectable) {
              this.selectRange(0, allOptions.length - 1);
            }
            evt.preventDefault();
            break;
          }
        // fall through
        default:
          if (evt.key.length === 1) {
            const itemToFocus = this.findItemToFocus(evt.key.toLowerCase());
            if (itemToFocus) {
              this.focusItem(itemToFocus);
            }
          }
          break;
      }
  
      if (this.activeDescendant !== lastActiveId) {
        this.updateScroll();
      }
    }
  
    findItemToFocus(character) {
      const itemList = this.listboxNode.querySelectorAll('[role="option"]');
      let searchIndex = 0;
  
      if (!this.keysSoFar) {
        for (let i = 0; i < itemList.length; i++) {
          if (itemList[i].getAttribute('id') == this.activeDescendant) {
            searchIndex = i;
          }
        }
      }
  
      this.keysSoFar += character;
      this.clearKeysSoFarAfterDelay();
  
      let nextMatch = this.findMatchInRange(
        itemList,
        searchIndex + 1,
        itemList.length
      );
  
      if (!nextMatch) {
        nextMatch = this.findMatchInRange(itemList, 0, searchIndex);
      }
      return nextMatch;
    }
  
    /* Return the index of the passed element within the passed array, or null if not found */
    getElementIndex(option, options) {
      const allOptions = Array.prototype.slice.call(options); // convert to array
      const optionIndex = allOptions.indexOf(option);
  
      return typeof optionIndex === 'number' ? optionIndex : null;
    }
  
    /* Return the next listbox option, if it exists; otherwise, returns null */
    findNextOption(currentOption) {
      const allOptions = Array.prototype.slice.call(
        this.listboxNode.querySelectorAll('[role="option"]')
      ); // get options array
      const currentOptionIndex = allOptions.indexOf(currentOption);
      let nextOption = null;
  
      if (currentOptionIndex > -1 && currentOptionIndex < allOptions.length - 1) {
        nextOption = allOptions[currentOptionIndex + 1];
      }
  
      return nextOption;
    }
  
    /* Return the previous listbox option, if it exists; otherwise, returns null */
    findPreviousOption(currentOption) {
      const allOptions = Array.prototype.slice.call(
        this.listboxNode.querySelectorAll('[role="option"]')
      ); // get options array
      const currentOptionIndex = allOptions.indexOf(currentOption);
      let previousOption = null;
  
      if (currentOptionIndex > -1 && currentOptionIndex > 0) {
        previousOption = allOptions[currentOptionIndex - 1];
      }
  
      return previousOption;
    }
  
    clearKeysSoFarAfterDelay() {
      if (this.keyClear) {
        clearTimeout(this.keyClear);
        this.keyClear = null;
      }
      this.keyClear = setTimeout(
        function () {
          this.keysSoFar = '';
          this.keyClear = null;
        }.bind(this),
        500
      );
    }
  
    findMatchInRange(list, startIndex, endIndex) {
      // Find the first item starting with the keysSoFar substring, searching in
      // the specified range of items
      for (let n = startIndex; n < endIndex; n++) {
        const label = list[n].innerText;
        if (label && label.toLowerCase().indexOf(this.keysSoFar) === 0) {
          return list[n];
        }
      }
      return null;
    }
  
    checkClickItem(evt) {
        if (evt.target.getAttribute('role') !== 'option') {
            return;
        }
    
        const clickedItem = evt.target;
        const isSelected = clickedItem.getAttribute('aria-selected') === 'true';
    
        if (!this.multiselectable) {
            // Deselect all other items if not multiselectable
            const allOptions = this.listboxNode.querySelectorAll('[role="option"]');
            allOptions.forEach(option => {
                option.setAttribute('aria-selected', 'false');
                option.classList.remove('selected');
                option.style.backgroundColor = ''; // Reset background color
                option.style.color = ''; // Reset text color
            });
        }
    
        // Toggle the selection state
        clickedItem.setAttribute('aria-selected', isSelected ? 'false' : 'true');
        clickedItem.classList.toggle('selected', !isSelected);
        clickedItem.style.backgroundColor = isSelected ? '' : '#09558B'; // Toggle background color
        clickedItem.style.color = isSelected ? '' : 'white'; // Toggle text color
    
        // Update the active descendant
        this.focusItem(clickedItem);
    
        // Update the move button state
        this.updateMoveButton();
    
        // Handle multiselectable range selection
        if (this.multiselectable && evt.shiftKey) {
            this.selectRange(this.startRangeIndex, clickedItem);
        }
    }
  
    checkMouseDown(evt) {
      if (
        this.multiselectable &&
        evt.shiftKey &&
        evt.target.getAttribute('role') === 'option'
      ) {
        evt.preventDefault();
      }
    }
  
    toggleSelectItem(element) {
        // Toggle the aria-selected value without deselecting other items
        const isSelected = element.getAttribute('aria-selected') === 'true';
        element.setAttribute('aria-selected', isSelected ? 'false' : 'true');
        this.updateMoveButton();
    }
  
    defocusItem(element) {
      if (!element) {
        return;
      }
      if (!this.multiselectable) {
        element.removeAttribute('aria-selected');
      }
      element.classList.remove('focused');
    }
  
    focusItem(element) {
      this.defocusItem(document.getElementById(this.activeDescendant));
      if (!this.multiselectable) {
        element.setAttribute('aria-selected', 'true');
      }
      element.classList.add('focused');
      this.listboxNode.setAttribute('aria-activedescendant', element.id);
      this.activeDescendant = element.id;
  
      if (!this.multiselectable) {
        this.updateMoveButton();
      }
  
      this.checkUpDownButtons();
      this.handleFocusChange(element);
    }
  
    checkInRange(index, start, end) {
      const rangeStart = start < end ? start : end;
      const rangeEnd = start < end ? end : start;
  
      return index >= rangeStart && index <= rangeEnd;
    }
  
    selectRange(start, end) {
      // get start/end indices
      const allOptions = this.listboxNode.querySelectorAll('[role="option"]');
      const startIndex =
        typeof start === 'number'
          ? start
          : this.getElementIndex(start, allOptions);
      const endIndex =
        typeof end === 'number' ? end : this.getElementIndex(end, allOptions);
  
      for (let index = 0; index < allOptions.length; index++) {
        const selected = this.checkInRange(index, startIndex, endIndex);
        allOptions[index].setAttribute('aria-selected', selected + '');
      }
  
      this.updateMoveButton();
    }
  
    updateMoveButton() {
      if (!this.moveButton) {
        return;
      }
  
      if (this.listboxNode.querySelector('[aria-selected="true"]')) {
        this.moveButton.setAttribute('aria-disabled', 'false');
      } else {
        this.moveButton.setAttribute('aria-disabled', 'true');
      }
    }
  
    updateScroll() {
      const selectedOption = document.getElementById(this.activeDescendant);
      if (selectedOption) {
        const scrollBottom =
          this.listboxNode.clientHeight + this.listboxNode.scrollTop;
        const elementBottom =
          selectedOption.offsetTop + selectedOption.offsetHeight;
        if (elementBottom > scrollBottom) {
          this.listboxNode.scrollTop =
            elementBottom - this.listboxNode.clientHeight;
        } else if (selectedOption.offsetTop < this.listboxNode.scrollTop) {
          this.listboxNode.scrollTop = selectedOption.offsetTop;
        }
        selectedOption.scrollIntoView({ block: 'nearest', inline: 'nearest' });
      }
    }

    checkUpDownButtons() {
      const activeElement = document.getElementById(this.activeDescendant);
  
      if (!this.moveUpDownEnabled) {
        return;
      }
  
      if (!activeElement) {
        this.upButton.setAttribute('aria-disabled', 'true');
        this.downButton.setAttribute('aria-disabled', 'true');
        return;
      }
  
      if (this.upButton) {
        if (activeElement.previousElementSibling) {
          this.upButton.setAttribute('aria-disabled', false);
        } else {
          this.upButton.setAttribute('aria-disabled', 'true');
        }
      }
  
      if (this.downButton) {
        if (activeElement.nextElementSibling) {
          this.downButton.setAttribute('aria-disabled', false);
        } else {
          this.downButton.setAttribute('aria-disabled', 'true');
        }
      }
    }
  
    addItems(items) {
      if (!items || !items.length) {
        return;
      }
  
      items.forEach(
        function (item) {
          this.defocusItem(item);
          this.toggleSelectItem(item);
          this.listboxNode.append(item);
        }.bind(this)
      );
  
      if (!this.activeDescendant) {
        this.focusItem(items[0]);
      }
  
      this.handleItemChange('added', items);
    }
  
    deleteItems() {
      let itemsToDelete;
  
      if (this.multiselectable) {
        itemsToDelete = this.listboxNode.querySelectorAll(
          '[aria-selected="true"]'
        );
      } else if (this.activeDescendant) {
        itemsToDelete = [document.getElementById(this.activeDescendant)];
      }
  
      if (!itemsToDelete || !itemsToDelete.length) {
        return [];
      }
  
      itemsToDelete.forEach(
        function (item) {
          item.remove();
  
          if (item.id === this.activeDescendant) {
            this.clearActiveDescendant();
          }
        }.bind(this)
      );
  
      this.handleItemChange('removed', itemsToDelete);
  
      return itemsToDelete;
    }
  
    clearActiveDescendant() {
      this.activeDescendant = null;
      this.listboxNode.setAttribute('aria-activedescendant', null);
  
      this.updateMoveButton();
      this.checkUpDownButtons();
    }
  
    moveUpItems() {
      if (!this.activeDescendant) {
        return;
      }
  
      const currentItem = document.getElementById(this.activeDescendant);
      const previousItem = currentItem.previousElementSibling;
  
      if (previousItem) {
        this.listboxNode.insertBefore(currentItem, previousItem);
        this.handleItemChange('moved_up', [currentItem]);
      }
  
      this.checkUpDownButtons();
    }
  
    moveDownItems() {
      if (!this.activeDescendant) {
        return;
      }
  
      var currentItem = document.getElementById(this.activeDescendant);
      var nextItem = currentItem.nextElementSibling;
  
      if (nextItem) {
        this.listboxNode.insertBefore(nextItem, currentItem);
        this.handleItemChange('moved_down', [currentItem]);
      }
  
      this.checkUpDownButtons();
    }
  
    moveItems() {
      if (!this.siblingList) {
        return;
      }
  
      var itemsToMove = this.deleteItems();
      this.siblingList.addItems(itemsToMove);
    }
  
    enableMoveUpDown(upButton, downButton) {
      this.moveUpDownEnabled = true;
      this.upButton = upButton;
      this.downButton = downButton;
      upButton.addEventListener('click', this.moveUpItems.bind(this));
      downButton.addEventListener('click', this.moveDownItems.bind(this));
    }
  
    setupMove(button, siblingList) {
      this.siblingList = siblingList;
      this.moveButton = button;
      button.addEventListener('click', this.moveItems.bind(this));
    }
  
    setHandleItemChange(handlerFn) {
      this.handleItemChange = handlerFn;
    }
  
    setHandleFocusChange(focusChangeHandler) {
      this.handleFocusChange = focusChangeHandler;
    }
  };
  
  'use strict';

  var aria = aria || {};
  
  window.addEventListener('load', function () {
    new aria.Listbox(document.getElementById('ss_elem_list'));
  });

// The button click function
function showAlert() { 
    alert('Button Clicked!');
}

// initialize clock
let clockInterval;
let secondsElapsed = 0;

// sets ups the clock  to display the runnning
function updateClock() {
  const hours = Math.floor(secondsElapsed / 3600).toString().padStart(2, '0');
  const minutes = Math.floor((secondsElapsed % 3600) / 60).toString().padStart(2, '0');
  const seconds = (secondsElapsed % 60).toString().padStart(2, '0');
  const timeString = `${hours}:${minutes}:${seconds}`;
  document.getElementById('clock').innerText = timeString;
  secondsElapsed++;
}

//Starts the clock
function startClock() {
    stopClock();
    secondsElapsed = 0;
    clockInterval = setInterval(updateClock, 1000);
}

//Stops the clock
function stopClock() {
  clearInterval(clockInterval);
  clockInterval = null;
}

// Initial setup of clock - displays clock
updateClock();
