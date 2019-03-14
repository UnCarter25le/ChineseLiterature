from django import template

register = template.Library()

@register.filter


def makeListAttachUrl(worksUrn):

    if  worksUrn != '["None"]' :
        worksUri = [ 'https://so.gushiwen.org'+ lists.replace('[','').replace(']','').replace('"','').replace(' ','') for lists in worksUrn.split(',')]
        if len(worksUri) > 1:
            return [worksUri[0],"\t...\t",worksUri[-1]]
        else:
            return worksUri
    else:
        return ["None"]