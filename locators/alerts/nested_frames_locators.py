class NestedFramesLocators:
    PARENT_FRAME = "iframe[srcdoc='<p>Parent frame</p>']"  # или #frame1 если есть id
    CHILD_FRAME = "iframe[srcdoc='<p>Child Iframe</p>']"  # или #frame2 если есть id
    PARENT_BODY = "body"
    CHILD_BODY = "body"
