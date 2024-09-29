//
//  CharactersModel.swift
//  Dattebayo
//
//  Created by Shaheem PP on 12/09/2024.
//

import Foundation

struct CharactersModel: Codable {
    let message: String
    let total: Int
    let characters: [Character]
}

struct Character: Codable, Identifiable {
    let id: Int?
    let name: String?
    let images: String?
//    var isLiked: Bool = false
}
