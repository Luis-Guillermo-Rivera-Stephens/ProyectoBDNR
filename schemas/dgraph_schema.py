import datetime
import json
import pydgraph

"""
    type Juego {
        _id
        name
        description
        category
        related_with
    }

    type Categoria {
        _id
        name
    }

    # Juego Properties
    _id: string @index(exact) . 
    name: string @index(term) . 
    description: string .       
    category: uid .             
    relatedWith: [uid] .        


    Categoria Properties
    _id: string @index(exact) . 
    name: string @index(term) . 

"""