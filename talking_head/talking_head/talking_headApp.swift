//
//  talking_headApp.swift
//  talking_head
//
//  Created by Kaspar on 22/08/2024.
//

import SwiftUI

@main
struct talking_headApp: App {
    let persistenceController = PersistenceController.shared

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.managedObjectContext, persistenceController.container.viewContext)
        }
    }
}
