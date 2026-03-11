#!/usr/bin/env python3
"""
Build ADR presentation from Red Hat template

This script creates the complete ADR presentation from scratch:
1. Copies Red Hat Consulting template
2. Removes unnecessary slides
3. Populates content slides
4. Applies formatting (bullets, bold)
5. Adds speaker notes

Usage:
    python scripts/build_presentation.py

Requirements:
    - credentials.json and token.json in parent directory
    - Red Hat template ID: 1B5s3eIrvbW7ZXDX0BH5qKb8b09pYudWyYPJUjw1ruQI
"""

import os
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configuration
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token_slides.json'  # Separate token for presentations
SCOPES = ['https://www.googleapis.com/auth/presentations', 'https://www.googleapis.com/auth/drive']

TEMPLATE_ID = '1B5s3eIrvbW7ZXDX0BH5qKb8b09pYudWyYPJUjw1ruQI'
NEW_TITLE = 'Architecture Decision Records in Consulting Delivery'

def get_credentials():
    """Get valid credentials, refreshing if needed"""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"❌ Error: {CREDENTIALS_FILE} not found")
                print("Please follow Google API setup instructions")
                sys.exit(1)

            print("Starting OAuth flow...")
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for next time
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
            print(f"✅ Token saved to {TOKEN_FILE}")

    return creds

def copy_template(service_drive, title):
    """Copy the Red Hat template"""
    try:
        # First, get info about the source file to check if it's on a Shared Drive
        source_file = service_drive.files().get(
            fileId=TEMPLATE_ID,
            fields='id,name,driveId',
            supportsAllDrives=True
        ).execute()

        print(f"   Source: {source_file.get('name')}")
        if source_file.get('driveId'):
            print(f"   Location: Shared Drive (ID: {source_file.get('driveId')})")

        # Copy the file (it will go to My Drive by default)
        copied_file = service_drive.files().copy(
            fileId=TEMPLATE_ID,
            body={'name': title},
            supportsAllDrives=True
        ).execute()

        presentation_id = copied_file.get('id')
        print(f"✅ Created presentation: {presentation_id}")
        return presentation_id
    except HttpError as error:
        print(f"❌ Error copying template: {error}")
        print("\nTroubleshooting:")
        print(f"  1. Verify template ID is correct: {TEMPLATE_ID}")
        print(f"  2. Check you have access to the template file")
        print(f"  3. Template might be in a Shared Drive with restricted copying")
        sys.exit(1)

def delete_slides(service, presentation_id, slide_indices):
    """Delete slides by index (0-based)"""
    try:
        presentation = service.presentations().get(presentationId=presentation_id).execute()
        slides = presentation.get('slides', [])

        slide_ids = [slides[i].get('objectId') for i in slide_indices if i < len(slides)]

        if not slide_ids:
            return

        requests = [{'deleteObject': {'objectId': sid}} for sid in slide_ids]

        service.presentations().batchUpdate(
            presentationId=presentation_id,
            body={'requests': requests}
        ).execute()

        print(f"✅ Deleted {len(slide_ids)} slides")
    except HttpError as error:
        print(f"❌ Error deleting slides: {error}")
        sys.exit(1)

def get_body_id(presentation, slide_id):
    """Get the BODY text box ID from a slide"""
    for slide in presentation.get('slides', []):
        if slide.get('objectId') == slide_id:
            for element in slide.get('pageElements', []):
                if 'shape' in element:
                    placeholder = element['shape'].get('placeholder', {})
                    if placeholder.get('type') == 'BODY':
                        return element.get('objectId')
    return None

def rebuild_slide_content(service, presentation_id, slide_id, body_id, content_structure):
    """Rebuild slide content with proper formatting"""
    try:
        requests = []

        # Delete existing text
        requests.append({
            'deleteText': {
                'objectId': body_id,
                'textRange': {'type': 'ALL'}
            }
        })

        # Insert new text
        full_text = '\n'.join([item['text'] for item in content_structure])
        requests.append({
            'insertText': {
                'objectId': body_id,
                'text': full_text,
                'insertionIndex': 0
            }
        })

        service.presentations().batchUpdate(
            presentationId=presentation_id,
            body={'requests': requests}
        ).execute()

        # Apply formatting in three phases
        delete_bullet_requests = []
        format_requests = []
        create_bullet_requests = []
        current_index = 0

        for item in content_structure:
            text_length = len(item['text']) + 1
            end_index = current_index + text_length - 1

            # Phase 1: Delete all bullets
            delete_bullet_requests.append({
                'deleteParagraphBullets': {
                    'objectId': body_id,
                    'textRange': {
                        'type': 'FIXED_RANGE',
                        'startIndex': current_index,
                        'endIndex': end_index
                    }
                }
            })

            # Phase 2: Apply bold if needed
            if item.get('bold', False):
                format_requests.append({
                    'updateTextStyle': {
                        'objectId': body_id,
                        'textRange': {
                            'type': 'FIXED_RANGE',
                            'startIndex': current_index,
                            'endIndex': end_index
                        },
                        'style': {'bold': True},
                        'fields': 'bold'
                    }
                })

            # Phase 3: Re-create bullets for level 1 and 2
            if item['level'] > 0:
                create_bullet_requests.append({
                    'createParagraphBullets': {
                        'objectId': body_id,
                        'textRange': {
                            'type': 'FIXED_RANGE',
                            'startIndex': current_index,
                            'endIndex': end_index
                        },
                        'bulletPreset': 'BULLET_DISC_CIRCLE_SQUARE'
                    }
                })

                indent_pt = 18 if item['level'] == 1 else 54

                format_requests.append({
                    'updateParagraphStyle': {
                        'objectId': body_id,
                        'textRange': {
                            'type': 'FIXED_RANGE',
                            'startIndex': current_index,
                            'endIndex': end_index
                        },
                        'style': {
                            'indentStart': {
                                'magnitude': indent_pt,
                                'unit': 'PT'
                            },
                            'indentFirstLine': {
                                'magnitude': 0,
                                'unit': 'PT'
                            }
                        },
                        'fields': 'indentStart,indentFirstLine'
                    }
                })

            current_index += text_length

        # Execute in order
        if delete_bullet_requests:
            service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': delete_bullet_requests}
            ).execute()

        if format_requests:
            service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': format_requests}
            ).execute()

        if create_bullet_requests:
            service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': create_bullet_requests}
            ).execute()

        return True

    except HttpError as error:
        print(f"❌ Error updating slide: {error}")
        return False

def add_speaker_notes(service, presentation_id, slide_id, notes_text):
    """Add speaker notes to a slide"""
    try:
        presentation = service.presentations().get(presentationId=presentation_id).execute()

        target_slide = None
        for slide in presentation.get('slides', []):
            if slide.get('objectId') == slide_id:
                target_slide = slide
                break

        if not target_slide:
            return False

        notes_page = target_slide.get('slideProperties', {}).get('notesPage', {})
        notes_body_id = None
        has_text = False

        for element in notes_page.get('pageElements', []):
            if 'shape' in element:
                placeholder = element['shape'].get('placeholder', {})
                if placeholder.get('type') == 'BODY':
                    notes_body_id = element.get('objectId')
                    text_content = element.get('shape', {}).get('text', {})
                    text_elements = text_content.get('textElements', [])
                    for te in text_elements:
                        if 'textRun' in te and te['textRun'].get('content', '').strip():
                            has_text = True
                            break
                    break

        if not notes_body_id:
            return False

        requests = []

        if has_text:
            requests.append({
                'deleteText': {
                    'objectId': notes_body_id,
                    'textRange': {'type': 'ALL'}
                }
            })

        requests.append({
            'insertText': {
                'objectId': notes_body_id,
                'text': notes_text,
                'insertionIndex': 0
            }
        })

        service.presentations().batchUpdate(
            presentationId=presentation_id,
            body={'requests': requests}
        ).execute()

        return True

    except HttpError as error:
        return False

def update_title_slide(service, presentation_id, slide_id):
    """Update the title slide with presentation details"""
    try:
        presentation = service.presentations().get(presentationId=presentation_id).execute()

        # Find the title slide
        title_slide = None
        for slide in presentation.get('slides', []):
            if slide.get('objectId') == slide_id:
                title_slide = slide
                break

        if not title_slide:
            return False

        requests = []
        subtitle_count = 0

        # Find and update text elements
        for element in title_slide.get('pageElements', []):
            if 'shape' not in element:
                continue

            shape = element['shape']
            placeholder = shape.get('placeholder', {})
            placeholder_type = placeholder.get('type')
            object_id = element.get('objectId')

            # Get current text
            text_content = shape.get('text', {})
            text_elements = text_content.get('textElements', [])
            full_text = ''
            for te in text_elements:
                if 'textRun' in te:
                    full_text += te['textRun'].get('content', '')

            # Update TITLE placeholder
            if placeholder_type == 'TITLE':
                requests.append({
                    'deleteText': {
                        'objectId': object_id,
                        'textRange': {'type': 'ALL'}
                    }
                })
                requests.append({
                    'insertText': {
                        'objectId': object_id,
                        'text': 'Architecture Decision Records in Consulting Delivery',
                        'insertionIndex': 0
                    }
                })

            # Update SUBTITLE placeholders (there are multiple!)
            elif placeholder_type == 'SUBTITLE':
                subtitle_count += 1
                if subtitle_count == 1:
                    # First subtitle = actual subtitle text
                    requests.append({
                        'deleteText': {
                            'objectId': object_id,
                            'textRange': {'type': 'ALL'}
                        }
                    })
                    requests.append({
                        'insertText': {
                            'objectId': object_id,
                            'text': 'A robust architecture design execution',
                            'insertionIndex': 0
                        }
                    })
                elif subtitle_count == 2:
                    # Second subtitle = presenter info
                    requests.append({
                        'deleteText': {
                            'objectId': object_id,
                            'textRange': {'type': 'ALL'}
                        }
                    })
                    requests.append({
                        'insertText': {
                            'objectId': object_id,
                            'text': 'Laurent TOURREAU\nEMEA Solution & Technology Practice',
                            'insertionIndex': 0
                        }
                    })
                else:
                    # Any additional subtitles = delete content
                    requests.append({
                        'deleteText': {
                            'objectId': object_id,
                            'textRange': {'type': 'ALL'}
                        }
                    })

        if requests:
            service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': requests}
            ).execute()
            return True

        return False

    except HttpError as error:
        print(f"⚠️ Warning: Could not update title slide: {error}")
        return False

def main():
    """Main function"""
    try:
        print("="*80)
        print("Building ADR Presentation from Template")
        print("="*80)

        # Get credentials
        creds = get_credentials()
        service_slides = build('slides', 'v1', credentials=creds)
        service_drive = build('drive', 'v3', credentials=creds)

        # Copy template
        print("\n1. Copying Red Hat template...")
        presentation_id = copy_template(service_drive, NEW_TITLE)

        # Get presentation structure
        presentation = service_slides.presentations().get(presentationId=presentation_id).execute()
        slides = presentation.get('slides', [])
        print(f"   Template has {len(slides)} slides")

        # Find the red "Thank you" closing slide (slide 20, index 19)
        closing_slide_index = None
        if len(slides) > 20:
            # Check slide 20 (index 19)
            test_slide = slides[19]
            # Try to identify by layout or content
            for element in test_slide.get('pageElements', []):
                if 'shape' in element:
                    shape = element['shape']
                    text_content = shape.get('text', {})
                    text_elements = text_content.get('textElements', [])
                    full_text = ''
                    for te in text_elements:
                        if 'textRun' in te:
                            full_text += te['textRun'].get('content', '')
                    if 'thank' in full_text.lower():
                        closing_slide_index = 19
                        print(f"   Found 'Thank you' slide at position 20")
                        break

        if closing_slide_index is None:
            # Fallback to last slide
            closing_slide_index = len(slides) - 1
            print(f"   Using last slide as closing")

        # Update title slide
        print("\n2. Updating title slide...")
        title_slide_id = slides[0].get('objectId')
        if update_title_slide(service_slides, presentation_id, title_slide_id):
            print("   ✅ Title slide updated")
        else:
            print("   ⚠️ Could not update title slide")

        # Delete unnecessary slides (keep slide 0=title, 1=content template, closing=slide 20)
        print("\n3. Removing unnecessary slides...")
        # Keep slides 0, 1, and closing slide, delete everything else
        slides_to_delete = []
        for i in range(len(slides)):
            if i not in [0, 1, closing_slide_index]:
                slides_to_delete.append(i)

        delete_slides(service_slides, presentation_id, slides_to_delete)

        # Refresh presentation
        presentation = service_slides.presentations().get(presentationId=presentation_id).execute()
        slides = presentation.get('slides', [])
        print(f"   Now has {len(slides)} slides")

        # Remove all non-placeholder shapes AND element groups from content template
        print("\n4. Cleaning content template slide...")
        content_template_slide = slides[1]
        delete_requests = []

        for element in content_template_slide.get('pageElements', []):
            # Delete ELEMENT_GROUP (Quick tip boxes are grouped elements)
            if 'elementGroup' in element:
                object_id = element.get('objectId')
                delete_requests.append({
                    'deleteObject': {
                        'objectId': object_id
                    }
                })
            # Delete non-placeholder shapes
            elif 'shape' in element:
                shape = element['shape']
                placeholder = shape.get('placeholder', {})
                placeholder_type = placeholder.get('type')

                # Keep only TITLE and BODY placeholders, delete everything else
                if not placeholder_type or placeholder_type not in ['TITLE', 'BODY', 'CENTERED_TITLE', 'SUBTITLE']:
                    object_id = element.get('objectId')
                    delete_requests.append({
                        'deleteObject': {
                            'objectId': object_id
                        }
                    })

        if delete_requests:
            service_slides.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': delete_requests}
            ).execute()
            print(f"   ✅ Removed {len(delete_requests)} element(s) (Quick tip boxes + others)")
        else:
            print("   Template is clean")

        # Refresh to get updated slide
        presentation = service_slides.presentations().get(presentationId=presentation_id).execute()
        slides = presentation.get('slides', [])

        # Change content template to use blank layout without Quick tip boxes
        print("\n5. Changing content slide layout...")
        content_template_id = slides[1].get('objectId')

        # Get presentation layouts
        presentation_full = service_slides.presentations().get(presentationId=presentation_id).execute()
        layouts = presentation_full.get('layouts', [])
        blank_layout = None

        # Find a layout without extra elements (BLANK or TITLE_AND_BODY without decorations)
        for layout in layouts:
            layout_props = layout.get('layoutProperties', {})
            display_name = layout_props.get('displayName', '').lower()
            layout_name = layout_props.get('name', '').lower()

            # Look for simple layouts
            if any(keyword in display_name or keyword in layout_name
                   for keyword in ['blank', 'title and body', 'title & body', 'caption']):
                # Check if this layout has minimal elements (no Quick tip boxes)
                if len(layout.get('pageElements', [])) <= 3:  # Usually just title + body + maybe background
                    blank_layout = layout.get('objectId')
                    print(f"   Found layout: {display_name}")
                    break

        # If we found a simpler layout, apply it
        if blank_layout:
            service_slides.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': [{
                    'updateSlideProperties': {
                        'objectId': content_template_id,
                        'fields': 'layoutObjectId',
                        'slideProperties': {
                            'layoutObjectId': blank_layout
                        }
                    }
                }]}
            ).execute()
            print(f"   ✅ Changed to simpler layout (no Quick tip boxes)")
        else:
            print(f"   ⚠️ No alternate layout found")

        # Refresh to get updated slide structure
        presentation = service_slides.presentations().get(presentationId=presentation_id).execute()
        slides = presentation.get('slides', [])

        # Duplicate content slide to create 8 content slides (slides 1-8)
        print("\n6. Creating content slides and positioning...")
        content_template_id = slides[1].get('objectId')
        red_closing_id = slides[2].get('objectId')

        # Duplicate content template 7 times (to have 8 content slides total including original)
        requests = []
        for i in range(7):
            requests.append({
                'duplicateObject': {
                    'objectId': content_template_id
                }
            })

        service_slides.presentations().batchUpdate(
            presentationId=presentation_id,
            body={'requests': requests}
        ).execute()

        # Refresh to get all slides
        presentation = service_slides.presentations().get(presentationId=presentation_id).execute()
        slides = presentation.get('slides', [])
        print(f"   Created {len(slides)} slides total (should be 10)")

        # Now reorganize: Title, Content x8, Red
        # Current order: Title(0), Content(1), Red(2), Copy1(3), Copy2(4), Copy3(5), Copy4(6), Copy5(7), Copy6(8), Copy7(9)
        # Want: Title(0), Content(1), Copy1(2), Copy2(3), Copy3(4), Copy4(5), Copy5(6), Copy6(7), Copy7(8), Red(9)

        # Move copies to positions 2-8, pushing Red to position 9
        copy_ids = [slides[i].get('objectId') for i in range(3, 10)]  # Copies 1-7

        move_requests = []
        for idx, copy_id in enumerate(copy_ids):
            move_requests.append({
                'updateSlidesPosition': {
                    'slideObjectIds': [copy_id],
                    'insertionIndex': 2 + idx  # Insert at positions 2, 3, 4, 5, 6, 7, 8
                }
            })

        service_slides.presentations().batchUpdate(
            presentationId=presentation_id,
            body={'requests': move_requests}
        ).execute()
        print("   ✅ Slides reorganized: 8 content slides + red closing at position 9")

        # Refresh to get final order
        presentation = service_slides.presentations().get(presentationId=presentation_id).execute()
        slides = presentation.get('slides', [])

        # Define slide titles - NEW ORDER: Real example after ADR Structure (slide 4)
        slide_titles = {
            1: "What Are ADRs?",
            2: "ADR Structure",
            3: "Real example",
            4: "ADR templates repository",
            5: "Why ADRs Matter?",
            6: "Who & When?",
            7: "Semi-automated design workflow",
        }

        # Define slide content - NEW ORDER
        slide_contents = {
            1: [  # Slide 2: What Are ADRs?
                {'text': 'Architecture Decision Records (ADRs) document strategic choices between valid architecture alternatives during design phases in our consulting engagement.', 'level': 0, 'bold': False},
                {'text': 'IT IS NOT: Configuration Checklist', 'level': 0, 'bold': True},
                {'text': '"Set parameter X to value Y"', 'level': 1},
                {'text': '"Enable feature Z because it\'s required"', 'level': 1},
                {'text': 'IT IS: REAL Architecture Decisions', 'level': 0, 'bold': True},
                {'text': '"KServe vs. Custom Deployment for model serving?"', 'level': 1},
                {'text': '"Internal PostgreSQL vs. External managed DB?"', 'level': 1},
                {'text': '"Fast channel (early features) vs. Stable (production)?"', 'level': 1},
            ],
            2: [  # Slide 3: ADR Structure
                {'text': 'Each ADR follows a strict format:', 'level': 0, 'bold': False},
                {'text': 'Title: Concise description', 'level': 1, 'bold': False},
                {'text': 'Architectural Question: What choice is being made?', 'level': 1, 'bold': False},
                {'text': 'Issue: Why is this decision needed?', 'level': 1, 'bold': False},
                {'text': 'Assumptions: Dependencies or prerequisites', 'level': 1, 'bold': False},
                {'text': 'Alternatives: 2+ viable options', 'level': 1, 'bold': False},
                {'text': 'Decision: #TODO# until decided', 'level': 1, 'bold': False},
                {'text': 'Justification: Why choose each alternative', 'level': 1, 'bold': False},
                {'text': 'Implications: Consequences, trade-offs, risks', 'level': 1, 'bold': False},
                {'text': 'Agreeing Parties: Customer + Red Hat roles', 'level': 1, 'bold': False},
            ],
            3: [  # Slide 4: Real example
                {'text': 'OCP-BASE-01: Cluster Isolation Strategy', 'level': 0, 'bold': True},
                {'text': 'Question: How to separate Dev/Test/Prod workloads?', 'level': 0, 'bold': False},
                {'text': 'Alternatives:', 'level': 0, 'bold': True},
                {'text': 'Consolidated (Single Cluster)', 'level': 1, 'bold': False},
                {'text': 'Prod/Non-Prod Split', 'level': 1, 'bold': False},
                {'text': 'Per-Environment', 'level': 1, 'bold': False},
                {'text': 'Decision: Separate by infrastructure type', 'level': 0, 'bold': True},
                {'text': 'OpenStack: General purpose/dev workloads', 'level': 1, 'bold': False},
                {'text': 'Bare Metal: Performance/prod with GPUs', 'level': 1, 'bold': False},
                {'text': 'Agreeing Parties:', 'level': 0, 'bold': True},
                {'text': 'J. Smith (AI/ML Platform Owner)', 'level': 1, 'bold': False},
                {'text': 'A. Johnson (Storage Expert)', 'level': 1, 'bold': False},
                {'text': 'M. Chen (Security Expert)', 'level': 1, 'bold': False},
            ],
            4: [  # Slide 5: ADR repository template
                {'text': 'ADR repository template: 291 Documented Decisions', 'level': 0, 'bold': True},
                {'text': 'https://github.com/redhat-ai-services/openshift-adr', 'level': 0, 'bold': False},
                {'text': 'OpenShift Container Platform:', 'level': 0, 'bold': True},
                {'text': 'OCP-BM: 58 (Bare Metal & Day 0)', 'level': 1, 'bold': False},
                {'text': 'OCP-NET: 44 (Networking)', 'level': 1, 'bold': False},
                {'text': 'OCP-SEC: 19, OCP-BASE: 15, OCP-MGT: 12', 'level': 1, 'bold': False},
                {'text': 'AI/ML & Data:', 'level': 0, 'bold': True},
                {'text': 'RHOAI-SM: 53 (OpenShift AI Self-Managed)', 'level': 1, 'bold': False},
                {'text': 'NVIDIA-GPU: 9 (GPU Operator)', 'level': 1, 'bold': False},
                {'text': 'Platform Services:', 'level': 0, 'bold': True},
                {'text': 'ODF: 9, TRACING: 8, PIPELINES: 8, VIRT: 7', 'level': 1, 'bold': False},
                {'text': 'OCP-OSP: 8, GITOPS: 6, NETOBSERV: 6, and more', 'level': 1, 'bold': False},
            ],
            5: [  # Slide 6: Why ADRs Matter?
                {'text': 'The Problem:', 'level': 0, 'bold': True},
                {'text': 'Workshops happen, decisions captured (Miro/paper)', 'level': 1, 'bold': False},
                {'text': 'NOT formalized into design doc ❌', 'level': 1, 'bold': False},
                {'text': 'Workshop outputs vanish', 'level': 1, 'bold': False},
                {'text': 'Consultants implement without context', 'level': 1, 'bold': False},
                {'text': 'The Opportunity:', 'level': 0, 'bold': True},
                {'text': '5 min per ADR to formalize workshop outputs', 'level': 1, 'bold': False},
                {'text': 'Complete design deliverables with rationale', 'level': 1, 'bold': False},
                {'text': 'Smoother handover, reduced disputes', 'level': 1, 'bold': False},
                {'text': 'Permanent record for future audits', 'level': 1, 'bold': False},
                {'text': 'Note: CER decommissioned, ADRs go in design docs', 'level': 0, 'bold': False},
            ],
            6: [  # Slide 7: Who & When?
                {'text': 'Three Consulting Phases:', 'level': 0, 'bold': True},
                {'text': 'Design (Architect)', 'level': 1, 'bold': False},
                {'text': 'Implementation (Consultant)', 'level': 1, 'bold': False},
                {'text': 'Enablement (Consultant)', 'level': 1, 'bold': False},
                {'text': 'ADR Workflow:', 'level': 0, 'bold': True},
                {'text': 'Preparation: Extract decision points from docs', 'level': 1, 'bold': False},
                {'text': 'Workshop: Present questions, capture decisions', 'level': 1, 'bold': False},
                {'text': 'Design: Formalize Miro → ADRs in design doc', 'level': 1, 'bold': False},
                {'text': 'Handover: Consultant gets full context', 'level': 1, 'bold': False},
                {'text': 'Best Practice: Workshop → Miro → ADRs → Diagrams', 'level': 0, 'bold': True},
            ],
            7: [  # Slide 8: Semi-automated design workflow
                {'text': 'Semi-automated design workflow', 'level': 0, 'bold': True},
                {'text': 'Interactive ADR Pack Generation', 'level': 0, 'bold': True},
                {'text': 'Select products from 19 available', 'level': 1, 'bold': False},
                {'text': 'Generate customer-specific ADR pack', 'level': 1, 'bold': False},
                {'text': 'Google Docs Integration', 'level': 0, 'bold': True},
                {'text': 'Real-time collaboration during workshops', 'level': 1, 'bold': False},
                {'text': 'Professional formatting with #TODO# highlighting', 'level': 1, 'bold': False},
                {'text': 'No manual copy/paste to design documents', 'level': 1, 'bold': False},
                {'text': 'Validation & Export', 'level': 0, 'bold': True},
                {'text': 'Check command validates completion', 'level': 1, 'bold': False},
                {'text': 'Export to markdown/HTML for design docs', 'level': 1, 'bold': False},
                {'text': 'Repository: github.com/redhat-ai-services/openshift-adr', 'level': 0, 'bold': False},
            ],
        }

        # Speaker notes - Complete sentences for presentation delivery
        speaker_notes = {
            0: """Welcome everyone. Today I'm going to show you why Architecture Decision Records, or ADRs, should be part of every design document. This is a ten-minute overview of what ADRs are, why they matter, and how to use them. At the end, I'll show you our ADR repository which contains two hundred ninety-one documented architectural decisions across all Red Hat products.""",

            1: """Architecture Decision Records document strategic architectural choices during the design phase of consulting engagements. They are not configuration checklists. A configuration checklist would say something like "set this parameter to this value" - there's only one right answer, no choice involved. Real architectural decisions have multiple valid alternatives. For example: Should we use KServe or a custom deployment for model serving? Should we use an internal PostgreSQL database or an external managed database? Should we use the fast update channel to get early features, or the stable channel for production readiness? These are real architectural decisions where we need to choose between two or more viable options.""",

            2: """Every Architecture Decision Record follows the same structure. It starts with a Title that concisely describes the decision. Then we have the Architectural Question, which defines what choice is being made. The Issue section explains why this decision is needed. Assumptions capture any dependencies or prerequisites. The Alternatives section lists two or more viable options. The Decision field starts as a TODO placeholder and gets filled in during workshops. The Justification section explains why you would choose each alternative. The Implications section describes the consequences, trade-offs, and risks for each option. Finally, Agreeing Parties captures who made the decision - both customer stakeholders and Red Hat roles. Each ADR follows this exact structure to ensure consistency across all products.""",

            3: """Let me show you a real ADR example. This is OCP-BASE-01: Cluster Isolation Strategy. The architectural question was: How do we separate development, test, and production workloads across OpenShift clusters? Three alternatives were presented during the workshop. Alternative one: Consolidated single cluster where everything runs together. Alternative two: Prod/Non-Prod split, where production is separate from everything else. Alternative three: Per-environment separation, where dev, test, and prod each get their own cluster. The decision made was to separate clusters based on infrastructure type. OpenStack would host general purpose and development workloads. Bare Metal would host performance-intensive production workloads with GPUs. The agreeing parties were captured: J. Smith as the AI/ML Platform Owner, A. Johnson as the Storage Expert, and M. Chen as the Security Expert. Names are obfuscated here for demo purposes, but in a real ADR you would use actual names and roles.""",

            4: """This is the ADR Template Repository, which contains two hundred ninety-one documented architectural decisions across all Red Hat products. It's available at github.com/redhat-ai-services/openshift-adr. Let me break down these numbers. OpenShift Container Platform ADRs cover the full platform lifecycle. The largest category is OCP-BM with fifty-eight decisions covering bare metal infrastructure and Day Zero installation. OCP-NET has forty-four networking decisions. Then we have OCP-SEC with nineteen, OCP-BASE with fifteen, and OCP-MGT with twelve decisions. For AI and ML capabilities, RHOAI-SM has fifty-three decisions covering all OpenShift AI self-managed components. NVIDIA-GPU has nine decisions for GPU operator configuration. Platform services cover data foundation with nine ADRs, distributed tracing with eight, CI/CD pipelines with eight, virtualization with seven, OpenStack installation with eight, GitOps with six, network observability with six, and more. Each of these two hundred ninety-one ADRs documents a real architectural choice made during actual customer engagements, with alternatives, justifications, and agreeing parties all captured.""",

            5: """So why do ADRs matter? Let me explain the problem. Architects already facilitate design workshops. Decisions get captured on Miro boards, on paper, on whiteboards. But here's what happens: those decisions are not formalized into the design document. The workshop outputs vanish after the design phase ends. Then consultants start implementation without understanding the context of why choices were made. This creates problems. Now, here's the opportunity. It takes just five minutes per ADR to formalize what was already captured in the workshop. Five minutes to turn that Miro board into a permanent design deliverable with full rationale. This gives you complete design deliverables, smoother handover to consultants, reduced disputes, and a permanent record for future audits. One important note: CER has been decommissioned. ADRs now go directly in design documents, not in a separate system.""",

            6: """Who creates ADRs and when? Consulting delivery has three phases. First is Design, which is done by the Architect. Second is Implementation, done by the Consultant. Third is Enablement, also done by the Consultant. Here's the ADR workflow. During Preparation, you extract decision points from Red Hat documentation. During the Workshop, you present architectural questions to the customer and explain the alternatives with their pros and cons. You capture the decisions on Miro or paper - this is already happening today. During the Design phase, you formalize those Miro captures into ADRs in the design document. This is the step that's missing today. During Handover, the consultant receives the design document with ADRs that explain the "why" behind every choice. Best practice is: Workshop leads to Miro, Miro leads to ADRs, ADRs lead to diagrams. This ensures nothing gets lost in the handover.""",

            7: """Now let me show you the automated workflow we've built. We have an interactive ADR pack generation tool. You run the script, select from nineteen available products, and it generates a customer-specific ADR pack. The tool integrates with Google Docs API for real-time collaboration. During the workshop, the customer and Red Hat team edit the Google Doc together. The system applies professional formatting automatically: yellow background highlighting for TODO markers, two-column tables, bold text processing. No manual copy and paste needed - everything goes directly into the shared document. After the workshop, you run the validation command to check completion. It detects any remaining TODO markers and validates the decision and agreeing parties fields. Then you export to markdown or HTML format ready to insert into the design document. The complete documentation is in the repository at github.com/redhat-ai-services/openshift-adr. Check out SETUP.md for quick installation and USER_MANUAL.md for the complete workflow guide. This automation saves approximately five hours per engagement by eliminating manual formatting and data entry.""",
        }

        # Populate content slides
        print("\n7. Populating content slides...")
        for slide_idx, content in slide_contents.items():
            slide = slides[slide_idx]
            slide_id = slide.get('objectId')

            # Update slide title first
            if slide_idx in slide_titles:
                title_id = None
                for element in slide.get('pageElements', []):
                    if 'shape' in element:
                        shape = element['shape']
                        placeholder = shape.get('placeholder', {})
                        if placeholder.get('type') == 'TITLE':
                            title_id = element.get('objectId')
                            break

                if title_id:
                    try:
                        service_slides.presentations().batchUpdate(
                            presentationId=presentation_id,
                            body={'requests': [
                                {'deleteText': {'objectId': title_id, 'textRange': {'type': 'ALL'}}},
                                {'insertText': {'objectId': title_id, 'text': slide_titles[slide_idx], 'insertionIndex': 0}}
                            ]}
                        ).execute()
                    except:
                        pass

            body_id = get_body_id(presentation, slide_id)

            if body_id:
                print(f"   Slide {slide_idx + 1}: Updating content...")
                if rebuild_slide_content(service_slides, presentation_id, slide_id, body_id, content):
                    print(f"   Slide {slide_idx + 1}: ✅ Content updated")

                    # Add speaker notes
                    if slide_idx in speaker_notes:
                        if add_speaker_notes(service_slides, presentation_id, slide_id, speaker_notes[slide_idx]):
                            print(f"   Slide {slide_idx + 1}: ✅ Speaker notes added")

        # Remove slide 10 (unused content template copy)
        print("\n8. Removing redundant slide 10...")
        presentation = service_slides.presentations().get(presentationId=presentation_id).execute()
        slides = presentation.get('slides', [])

        if len(slides) > 9:
            # Slide 10 exists, delete it
            slide_10_id = slides[9].get('objectId')  # Index 9 = slide 10
            service_slides.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': [{
                    'deleteObject': {
                        'objectId': slide_10_id
                    }
                }]}
            ).execute()
            print("   ✅ Removed redundant slide 10")
        else:
            print("   No redundant slide found")

        # Final cleanup: Remove any remaining Quick tip boxes
        print("\n9. Final cleanup - checking for Quick tip boxes...")
        presentation = service_slides.presentations().get(presentationId=presentation_id).execute()
        delete_requests = []

        for slide in presentation.get('slides', []):
            for element in slide.get('pageElements', []):
                if 'shape' not in element:
                    continue

                shape = element['shape']
                placeholder = shape.get('placeholder', {})

                # Skip placeholders (title, body, etc.)
                if placeholder.get('type'):
                    continue

                # Get shape properties to check background color
                shape_props = shape.get('shapeProperties', {})
                shape_fill = shape_props.get('shapeBackgroundFill', {})
                solid_fill = shape_fill.get('solidFill', {})
                color = solid_fill.get('color', {})
                rgb = color.get('rgbColor', {})

                # Check text content
                text_content = shape.get('text', {})
                text_elements = text_content.get('textElements', [])
                full_text = ''
                for te in text_elements:
                    if 'textRun' in te:
                        full_text += te['textRun'].get('content', '')

                # Delete if it's a blue box OR contains "Quick tip" text
                is_blue = (rgb.get('blue', 0) > 0.5)
                has_quick_tip = 'quick tip' in full_text.lower() or 'Quick tip' in full_text

                if (is_blue and has_quick_tip) or has_quick_tip:
                    object_id = element.get('objectId')
                    delete_requests.append({
                        'deleteObject': {
                            'objectId': object_id
                        }
                    })

        if delete_requests:
            service_slides.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': delete_requests}
            ).execute()
            print(f"   ✅ Removed {len(delete_requests)} 'Quick tip' box(es)")
        else:
            print("   No 'Quick tip' boxes found")

        print("\n" + "="*80)
        print("✅ Presentation built successfully")
        print("="*80)
        print(f"\n🔗 View: https://docs.google.com/presentation/d/{presentation_id}/edit")
        print(f"\nPresentation ID: {presentation_id}")
        print("\n📊 Structure (9 slides):")
        print("   Slide 1: Title")
        print("   Slide 2: What Are ADRs?")
        print("   Slide 3: ADR Structure")
        print("   Slide 4: Real example")
        print("   Slide 5: ADR templates repository")
        print("   Slide 6: Why ADRs Matter?")
        print("   Slide 7: Who & When?")
        print("   Slide 8: Semi-automated design workflow")
        print("   Slide 9: Thank you (Red closing)")
        print("\n💡 Next steps:")
        print("   - Review speaker notes for presentation delivery")
        print("   - Test presentation flow and timing")

    except HttpError as error:
        print(f"❌ An error occurred: {error}")
        sys.exit(1)

if __name__ == '__main__':
    main()
